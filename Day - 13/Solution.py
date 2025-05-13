# Day 13
# Challenge: Script to create and destroy Docker containers.
# Focus: docker-py SDK
# Example Hint: Connect to local Docker daemon

import uuid
import docker
import time

def manage_containers():
    # Connect to the local Docker daemon
    client = docker.from_env()
    try:
        print("Connected to Docker daemon")
        print(f"Docker server version: {client.version()['Version']}")
        
        # Pull a lightweight image (alpine) if not already present
        image_name = "alpine:latest"
        print(f"\nPulling image {image_name}...")
        client.images.pull("alpine", tag="latest")
        
        # Generate a unique container name
        unique_name = f"demo_container_{uuid.uuid4().hex[:8]}"
        
        # Remove existing container with the same name if it exists
        try:
            existing = client.containers.get(unique_name)
            print(f"Container with name `{unique_name}` already exists. Removing it...")
            existing.remove(force=True)
        except docker.errors.NotFound:
            pass

        # Create a container with resource limits and safe command
        print("\nCreating container...")
        container = client.containers.run(
            image_name,
            name=unique_name,
            command=["sh", "-c", "for i in $(seq 1 5); do echo Hello $i; sleep 1; done"],
            detach=True,
            mem_limit="128m",
            cpu_shares=256
        )
        print(f"Created container with ID: {container.id}")
        print(f"Container name: {container.name}")
        print(f"Container status: {container.status}")
        
        # Monitor container logs in real-time
        print("\nStreaming container logs:")
        for line in container.logs(stream=True):
            print(line.decode('utf-8').strip())
        
        # Wait for container to stop
        while container.status == "running":
            print(f"Waiting for container to finish (status: {container.status})...")
            time.sleep(1)
            container.reload()  # Refresh container state
        
        print(f"\nContainer finished with status: {container.status}")
        print(f"Exit code: {container.attrs['State']['ExitCode']}")
        
        # Remove the container
        print("\nRemoving container...")
        container.remove()
        print("Container removed successfully")
    finally:
        client.close()

if __name__ == "__main__":
    try:
        manage_containers()
    except docker.errors.DockerException as e:
        print(f"Error interacting with Docker: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
