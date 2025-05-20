# Jenkins Trigger API                                                                                                                                      

A comprehensive Flask API to trigger Jenkins jobs remotely using HTTP POST requests with Basic Authentication and parameter support. This project is designed to bridge the gap between Jenkins and external applications by providing a simple, secure, and extensible REST API.

---

## Overview

This project provides a REST API to trigger Jenkins jobs via HTTP POST requests. It implements Basic Authentication to secure endpoints and allows passing job parameters in JSON format. It is particularly useful for automating Jenkins job execution from external services or scripts.

---

## Features

* Trigger Jenkins jobs with parameters.
* Basic HTTP Authentication to protect endpoints.
* Health check endpoint for monitoring.
* Custom error handling and response formatting.
* Environment variable configuration.

---

## Project Structure

* `run.py` — Entry point to start the Flask server.
* `config.py` — Handles environment variable loading and configuration settings.
* `app/__init__.py` — Creates and configures the Flask application instance.
* `app/routes.py` — Defines API routes and their logic.
* `app/services/jenkins_service.py` — Handles communication with Jenkins.
* `app/utils/auth.py` — Implements basic authentication.
* `.env` — Environment configuration file (excluded from repo for security).

---

## Setup Instructions

### Prerequisites

* Python 3.8 or above
* Pip
* Jenkins server with job(s) configured
* WSL or Docker (if using on Windows)

### 1. Clone the repository:

```bash
 git clone <repo_url>
 cd <repo_directory>
```

### 2. Create a `.env` file in the project root with the following variables:

```ini
# Jenkins Configuration
JENKINS_URL=http://localhost:8080
JENKINS_USERNAME=your_jenkins_username
JENKINS_API_TOKEN=your_jenkins_api_token

# Flask Basic Auth
BASIC_AUTH_USERNAME=api-user
BASIC_AUTH_PASSWORD=secure-password

# Flask Configuration
FLASK_SECRET_KEY=your_flask_secret_key
FLASK_ENV=development
```

### 3. Install dependencies:

```bash
pip install -r requirements.txt
```

### 4. Run the Flask application:

```bash
python run.py
```

If using WSL, confirm the app is accessible through the correct IP (e.g., `172.x.x.x`).

---

## Usage Instructions

### Health Check Endpoint:

```bash
curl http://localhost:5000/health
```

Expected response:

```json
{"status": "healthy"}
```

### Trigger Jenkins Job:

1. Encode the credentials to Base64:

```bash
echo -n 'api-user:secure-password' | base64
```

2. Trigger the job:

```bash
curl -X POST http://localhost:5000/trigger-job/job-name \
  -H "Authorization: Basic <base64_encoded_credentials>" \
  -H "Content-Type: application/json" \
  -d '{"param1": "value1", "param2": "value2"}'
```

---

## Common Issues and Solutions

### 1. Connection Refused Error:

* **Cause:** Flask app bound to `127.0.0.1` instead of `0.0.0.0`.
* **Solution:** Update `run.py` to use `0.0.0.0`:

```python
app.run(host='0.0.0.0', port=5000)
```

---

### 2. Authentication Errors:

* **Cause:** Incorrect Base64 encoding or mismatched credentials.
* **Solution:** Verify `.env` variables and use correct encoding:

```bash
echo -n 'api-user:secure-password' | base64
```

---

### 3. Network Issues in WSL/Docker:

* **Cause:** Different IP addresses in Windows, WSL, and Docker.
* **Solution:** Identify the correct IP using:

```bash
ipconfig
```

Access the app using the specific IP, e.g., `172.x.x.x`.

---

### 4. Missing Dependencies:

* **Cause:** Dependencies not installed correctly.
* **Solution:** Run:

```bash
pip install -r requirements.txt
```

---

## Code Explanation

### `run.py`

* Entry point for running the Flask app.
* Loads the app instance from `app/__init__.py`.
* Runs on all interfaces (`0.0.0.0`) to handle requests from different networks.

### `app/__init__.py`

* Creates the Flask app.
* Loads environment variables using `dotenv`.
* Registers API blueprint (`app/routes.py`).

### `app/routes.py`

* Defines `/trigger-job` endpoint to handle POST requests.
* Implements basic auth using the `@basic_auth_required` decorator.
* Passes job parameters to Jenkins via `jenkins_service.py`.

### `app/services/jenkins_service.py`

* Handles Jenkins API interactions.
* Constructs the Jenkins job URL using the job name and parameters.
* Sends the request with authentication.

### `app/utils/auth.py`

* Implements Basic Authentication using environment variables.
* Decodes the `Authorization` header and validates credentials.

---

## Testing and Debugging

* Run the application in debug mode to view detailed error logs:

```bash
export FLASK_ENV=development
python run.py
```

* Inspect network interfaces and active ports using:

```bash
ipconfig
netstat -an | findstr 5000
```

---

## Summary

This API provides a simple interface to trigger Jenkins jobs with parameter support and basic authentication. It is designed to be platform-agnostic but may require specific configuration for WSL, Docker, or native Windows setups. Detailed troubleshooting and setup steps have been included to minimize connectivity and authentication issues.

For further improvements, consider implementing token-based authentication, detailed logging, and more robust error handling.
