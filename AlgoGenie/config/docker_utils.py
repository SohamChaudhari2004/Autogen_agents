async def start_docker(docker):
    print("Starting Docker container...")
    await docker.start()

async def stop_docker(docker):
    print("Stopping Docker container...")
    await docker.stop()
    print("Docker container stopped.")