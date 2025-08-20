from __future__ import annotations
import arxiv
from autogen_agentchat.agents import AssistantAgent
from autogen_core.tools import FunctionTool
from typing import List, Optional, AsyncGenerator , Dict
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.messages import (
    TextMessage,
    ToolCallExecutionEvent,
    ToolCallRequestEvent
)
from autogen_agentchat.teams import RoundRobinGroupChat
import os
from dotenv import load_dotenv
import asyncio
load_dotenv()

# =============================================
# Tools
# =============================================

def arxiv_search(query: str, max_results: int = 5) -> List[Dict]:
    """
    Returns a list of search results from the arXiv API matching the {query}.
    Each element contains `title`, `summary`, `authors`, `published`, and `pdf_url`.
    The helper is wrapped as an Autogen FunctionTool below so it can be invoked by the agents using normal tool-use mechanisms.

    """
    client = arxiv.Client()
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance
    )

    papers: List[Dict] = []

    for res in client.results(search):
        papers.append({
            "title": res.title,
            "summary": res.summary,
            "authors": [author.name for author in res.authors],
            "published": res.published.strftime("%Y-%m-%d"),
            "pdf_url": res.pdf_url
        })
    return papers


arxiv_search_tool = FunctionTool(
    arxiv_search,
    description="""Searches arXiv and returns up to papers, each containing "title, authors, publication date, abstract, and pdf_url."
"""
)


# =========================================
# TEAM BUILDING
# ==========================================
gemini_api_key = os.getenv('GEMINI_API_KEY')

model_client = OpenAIChatCompletionClient(
    model="gemini-2.5-pro",
    api_key= gemini_api_key,
    model_info={
        "vision": "enabled",
        "text": "enabled",
        "family": 'gemini-2.5-pro',
        'function_calling': "enabled",
        'json_output': "enabled",
        'multiple_system_messages': "enabled",
        'structured_output': "enabled"
    }
)


def build_team() -> RoundRobinGroupChat:

    llm_client = model_client
    search_agent = AssistantAgent(
        tools=[arxiv_search_tool],
        name="SearchAgent",
        system_message="""
"Given a user topic, think of the best arXiv query and call the '
"provided tool. Always fetch five times the papers requested so
"that you can downselect the most relevant ones. When the tool
returns, choose exactly the number of papers requested and pass
"them as concise to the summarizer. "
    """
        ,
        model_client=model_client,
        reflect_on_tool_use=True

    )



    summarizer = AssistantAgent(
        name="Summarizer_agent",
        model_client=model_client,
        description="Summarizes the key findings from the selected papers and provides a concise markdown review from provided papers.",
        system_message="""
            You are an expert researcher. When you receive the JSON list of papers, write a literature review style report in Markdown:
            1. Start with a sentence introduction of the topic.
            2. Then include one bullet per paper with: title (as Markdown link), authors, the specific problem tackled, and its key contribution.
            3. Close with a single sentence takeaway.
        """
    )

    return RoundRobinGroupChat(
        participants=[search_agent, summarizer],
        max_turns=2
    )



# =========================================
# ORCHESTRATION
# ==========================================

async def run_lit_review_agent(
        topic: str,
        max_results: int = 5,
        model : str = "gemini-2.5-flash"
)-> AsyncGenerator[str, None]:
    team = build_team()
    task_prompt  = f"conduct a literature review on {topic} with a maximum of {max_results} results."
    
    async for msg in team.run_stream(task=task_prompt):
        if isinstance(msg, TextMessage):
            yield f"{msg.source}:{msg.content}"

# =========================================
# TEST
# ==========================================


if __name__ == "__main__":
    topic = "large language models"
    
    async def main():
        # Consume the async generator and print each yielded result
        async for message in run_lit_review_agent(topic=topic, max_results=5, model="gemini-2.5-flash"):
            print(message)
    
    # Run the main coroutine
    asyncio.run(main())