from autogen_agentchat.teams import RoundRobinGroupChat
from agents.code_exec import get_code_executor_agent
from agents.problem_solver import get_problem_solver_agent
from config.constant import TEXT_MENTION, MAX_TURNS
from autogen_agentchat.conditions import TextMentionTermination


def get_dsa_team_and_docker():

    problem_solver_agent= get_problem_solver_agent()
    code_executor_agent , docker = get_code_executor_agent()

    termination_condition = TextMentionTermination(TEXT_MENTION)

    team = RoundRobinGroupChat(
        participants=[
            problem_solver_agent,
            code_executor_agent
        ],
        termination_condition=termination_condition,
        max_turns=MAX_TURNS
    )

    return team,docker