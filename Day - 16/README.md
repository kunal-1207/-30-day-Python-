# Prometheus Alert Fetcher

A Python script to fetch and display top active alerts from a Prometheus server using its API.

## 📦 Features

* Connect to a Prometheus server and verify its health status.
* Fetch all active alerts (state: 'firing').
* Display alerts in a structured format with name, severity, state, and summary.
* Provides troubleshooting tips in case of connection failure.

## 🛠️ Prerequisites

* Python 3.x
* Prometheus server running and accessible
* Internet connection (for fetching alerts)

## 🛠️ Dependencies

* `requests` library

Install dependencies:

```bash
pip install requests
```

## 🚀 How to Run

### 1. Clone this repository:

```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Update the configuration values in the script:

* `PROMETHEUS_URL`: URL of the Prometheus server (e.g., `http://localhost:9090`).
* `TIMEOUT`: Connection timeout in seconds.
* `USERNAME` and `PASSWORD`: Uncomment and update if authentication is required.

### 3. Run the script:

```bash
python alert_fetcher.py
```

## 🐳 Running Prometheus in Docker

Run Prometheus locally using Docker:

```bash
docker run -p 9090:9090 prom/prometheus
```

Access the Prometheus web UI at [http://localhost:9090](http://localhost:9090).

## 📝 Code Breakdown

### Configuration

```python
PROMETHEUS_URL = "http://localhost:9090"  # Change to your Prometheus server
ALERTS_ENDPOINT = "/api/v1/alerts"
TIMEOUT = 5  # seconds
```

* `PROMETHEUS_URL`: Base URL for the Prometheus server.
* `ALERTS_ENDPOINT`: API endpoint for alerts.
* `TIMEOUT`: Request timeout duration.

### Authentication

```python
# USERNAME = "your_username"
# PASSWORD = "your_password"
```

* Uncomment and set these values if authentication is required.

### Testing the Connection

```python
def test_prometheus_connection():
    health_url = f"{PROMETHEUS_URL}/-/healthy"
```

* Verifies the health status of the Prometheus server using the `/-/healthy` endpoint.

### Fetching Active Alerts

```python
def get_active_alerts():
    url = f"{PROMETHEUS_URL}{ALERTS_ENDPOINT}"
```

* Connects to the `/api/v1/alerts` endpoint to fetch active alerts.
* Filters alerts in the `firing` state.

### Displaying Alerts

```python
def display_alerts(alerts):
```

* Formats and prints alert details, including name, severity, state, and active duration.

### Main Function

```python
if __name__ == "__main__":
    main()
```

* Entry point for executing the script.

## ✅ Troubleshooting

* Verify Prometheus server URL.
* Check network/firewall settings.
* Update authentication credentials if required.
* Increase the timeout value if necessary.

## 🛠️ Pros and Cons of Running in WSL vs. Windows

### ✅ Pros of WSL:

* Unix-like environment, making it easier to manage dependencies.
* Easier to run Docker containers.
* Native Bash scripting support.

### ❌ Cons of WSL:

* Potential network configuration issues.
* File path differences may cause errors.
* Requires enabling WSL and Docker Desktop.

### ✅ Pros of Windows:

* Easier setup for Python without WSL configuration.
* Direct access to Windows filesystem.

### ❌ Cons of Windows:

* Dependency management can be more complex.
* Docker may require additional configuration.
* Some Unix-based commands may not work as expected.

## 🚧 Problems Encountered

* Network connection errors due to incorrect Prometheus URL.
* Authentication failures when the server required credentials.
* Docker not starting properly in WSL due to incorrect permissions.

## 📜 License

This project is licensed under the MIT License.
