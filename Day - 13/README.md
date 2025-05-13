## Script to Create and Destroy Docker Containers

This Python script is designed to demonstrate the management of Docker containers using the `docker-py` SDK. It connects to the local Docker daemon, pulls a lightweight Docker image (`alpine:latest`), creates a container with resource limits, executes a simple command, streams the container logs in real-time, and then removes the container upon completion.

---

## ✅ **Requirements:**

* Python 3.x
* Docker installed and running locally
* `docker-py` library

Install the required library:

```bash
pip install docker
```

---

## 🚀 **Usage:**

1. Clone this repository:

   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Ensure Docker is running on your system.

3. Run the script:

   ```bash
   python manage_containers.py
   ```

---

## 🛠️ **How It Works:**

### **1. Import Necessary Libraries:**

```python
import uuid
import docker
import time
```

* **`uuid`**: Generates unique identifiers for container names.
* **`docker`**: Provides the Docker SDK for Python.
* **`time`**: Adds delays for monitoring and controlling the container lifecycle.

---

### **2. Define the `manage_containers()` Function:**

This function encapsulates the entire container lifecycle management logic.

```python
def manage_containers():
```

* Connects to the Docker daemon.
* Pulls a Docker image.
* Creates a container.
* Monitors and logs the container's output.
* Removes the container upon completion.

---

### **3. Connect to Docker Daemon:**

```python
client = docker.from_env()
```

* Establishes a connection to the local Docker daemon using the environment configuration.

---

### **4. Display Docker Server Version:**

```python
print(f"Docker server version: {client.version()['Version']}")
```

* Retrieves and prints the Docker server version for reference.

---

### **5. Pull Docker Image:**

```python
image_name = "alpine:latest"
client.images.pull("alpine", tag="latest")
```

* Pulls the latest `alpine` image, a minimal Linux distribution, if not already present.

---

### **6. Generate Unique Container Name:**

```python
unique_name = f"demo_container_{uuid.uuid4().hex[:8]}"
```

* Creates a unique name using a random UUID to avoid naming conflicts.

---

### **7. Remove Existing Container (if any):**

```python
try:
    existing = client.containers.get(unique_name)
    existing.remove(force=True)
except docker.errors.NotFound:
    pass
```

* Checks if a container with the generated name already exists and removes it to prevent conflicts.

---

### **8. Create and Start the Container:**

```python
container = client.containers.run(
    image_name,
    name=unique_name,
    command=["sh", "-c", "for i in $(seq 1 5); do echo Hello $i; sleep 1; done"],
    detach=True,
    mem_limit="128m",
    cpu_shares=256
)
```

* Creates and starts a container with the following specifications:

  * **Image:** `alpine:latest`
  * **Command:** Prints "Hello" followed by a number (1-5) with a 1-second interval.
  * **Memory Limit:** 128 MB
  * **CPU Shares:** 256 (relative weight for CPU allocation)

---

### **9. Stream Container Logs:**

```python
for line in container.logs(stream=True):
    print(line.decode('utf-8').strip())
```

* Streams the container logs in real-time, displaying each line of output as it is produced.

---

### **10. Wait for Container Completion:**

```python
while container.status == "running":
    time.sleep(1)
    container.reload()
```

* Continuously checks the container status and waits until it exits.

---

### **11. Display Exit Code and Remove the Container:**

```python
print(f"Exit code: {container.attrs['State']['ExitCode']}")
container.remove()
```

* Prints the container's exit code and removes the container after completion.

---

### **12. Exception Handling:**

```python
except docker.errors.DockerException as e:
    print(f"Error interacting with Docker: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
```

* Catches and handles potential exceptions related to Docker interactions and general execution errors.

---

### **13. Entry Point:**

```python
if __name__ == "__main__":
    manage_containers()
```

* Ensures the script only runs when executed directly, not when imported as a module.

---

## ✅ **Expected Output:**

When you run the script, the output will look similar to the following:

```
Connected to Docker daemon
Docker server version: 24.0.1

Pulling image alpine:latest...
Creating container...
Created container with ID: <container_id>
Container name: demo_container_<random_uuid>
Container status: created

Streaming container logs:
Hello 1
Hello 2
Hello 3
Hello 4
Hello 5

Container finished with status: exited
Exit code: 0

Removing container...
Container removed successfully
```

---

## 📚 **Further Reading:**

* [Docker SDK for Python](https://docker-py.readthedocs.io/en/stable/)
* [Docker Documentation](https://docs.docker.com/)

---



