from autogen_agentchat.agents import CodeExecutorAgent
from config.docker_executer import get_docker_executor

def get_code_executor_agent():
    '''
    This function will get the docker executor function to get the docker command line code executor
    This agent will be responsible for executing code in a docker container
    This agent will coordinate with the problem_solver agent to execute the code
    '''
    docker = get_docker_executor()
    code_executor_agent = CodeExecutorAgent(
        name="CodeExecutorAgent",
        code_executor=docker
    )

    return code_executor_agent, docker