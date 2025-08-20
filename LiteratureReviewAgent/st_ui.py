import streamlit as st
import asyncio


from agent import run_lit_review_agent

st.set_page_config(page_title="Literature Review Agent", layout="wide")
st.title("Literature Review Agent")

query = st.text_input("Enter your research topic:")
max_papers = st.slider("Number of papers to review:", min_value=1, max_value=10, value=5)

if st.button('search') and query:

    async def runner() -> None:
        chat_placeholder = st.container()
        async for frame in run_lit_review_agent(topic=query, max_results=max_papers):
            role , *rest= frame.split(":", 1)
            content  = rest[0].strip() if rest else ""
            with chat_placeholder:
                with st.chat_message("assistant"):
                    st.markdown(f"**{role}**: {content}")
                    
    with st.spinner("Searching..."):
        try:
            asyncio.run(runner())
        except Exception as e:
            st.error(f"Error: {e}")

    