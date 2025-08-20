from autogen_ext.code_executors.docker import DockerCommandLineCodeExecutor
from config.constant import WORK_DIR , TIMEOUT

def get_docker_executor():
    '''
    function to get the docker command line code executor
    This will run the code in docker container
    '''
    docker_executor =  DockerCommandLineCodeExecutor(
        work_dir=WORK_DIR,
        timeout=TIMEOUT
    )

    return docker_executor
