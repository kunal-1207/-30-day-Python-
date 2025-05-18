# Jenkins Trigger API

A simple Flask API to trigger Jenkins jobs remotely with basic authentication and parameter support.

---

## Overview

This project provides a REST API to trigger Jenkins jobs via HTTP POST requests. It supports basic authentication for security and allows passing job parameters in JSON format.

---

## Features

* Trigger Jenkins jobs with parameters.
* Basic HTTP Authentication.
* Health check endpoint.
* Configurable via environment variables.

---

## Contents

* `run.py` — Entry point to start the Flask server.
* `config.py` — Loads environment variables and configuration settings.
* `app/__init__.py` — Creates and configures the Flask app.
* `app/routes.py` — Defines API routes and their logic.
* `app/services/jenkins_service.py` — Handles communication with Jenkins.
* `app/utils/auth.py` — Basic authentication decorator.
* `.env` — Environment configuration file (excluded from repo for security).

---

## Setup Instructions

1. **Clone the repository** and navigate to the project folder.

2. **Create a `.env` file** (not committed to version control) with these variables:

   ```ini
   JENKINS_URL=your_jenkins_url
   JENKINS_USERNAME=your_jenkins_username
   JENKINS_API_TOKEN=your_jenkins_api_token

   BASIC_AUTH_USERNAME=api-user
   BASIC_AUTH_PASSWORD=secure-password

   FLASK_SECRET_KEY=your_flask_secret_key
   FLASK_ENV=development
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Flask app:**

   ```bash
   python run.py
   ```

   The app listens on all interfaces (`0.0.0.0`) at port `5000`.

---

## How to Use the API

* Health check:

  ```bash
  curl http://localhost:5000/health
  ```

* Trigger a Jenkins job:

  ```bash
  curl -X POST http://localhost:5000/trigger-job/job-name \
    -H "Authorization: Basic <base64_encoded_credentials>" \
    -H "Content-Type: application/json" \
    -d '{"param1":"value1", "param2":"value2"}'
  ```

---

## Problems Faced and Solutions

### 1. **Connection refused when curling `localhost:5000`**

* **Cause:** Flask app was bound to `127.0.0.1` (localhost) but running inside a container or WSL, making it inaccessible from host or other network interfaces.

* **Solution:** Changed Flask app to run on `0.0.0.0` to listen on all network interfaces:

  ```python
  app.run(host='0.0.0.0', port=5000)
  ```

* Also ensured port forwarding was correctly set up in container/devcontainer config.

---

### 2. **Basic Authentication errors despite sending Authorization header**

* **Cause:** Incorrect or missing authentication headers in requests; mismatch between credentials and environment variables.
* **Solution:**

  * Verified correct username and password in `.env`.

  * Created base64 encoded string for `"username:password"` correctly (without trailing newline).

  * Used proper `Authorization` header format:

    ```
    Authorization: Basic <base64-encoded-credentials>
    ```

  * Ensured the Flask app uses a custom `@basic_auth_required` decorator instead of Flask extensions that might interfere.

---

### 3. **Inconsistent IP addresses between host and container/WSL**

* **Cause:** `localhost` inside WSL or containers is different from Windows host `localhost`.
* **Solution:** Used the actual IP address of the host network adapter to reach the Flask app from different environments.

---

## Code Explanation

### `run.py`

Entry point to start the Flask app:

```python
from app import create_app
import os

app = create_app()

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
```

* Loads the Flask app.
* Runs it on all network interfaces on port 5000 (or port from environment variable).

---

### `config.py`

Loads configuration from environment variables:

```python
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    JENKINS_URL = os.getenv('JENKINS_URL', 'http://localhost:8080')
    JENKINS_USERNAME = os.getenv('JENKINS_USERNAME')
    JENKINS_API_TOKEN = os.getenv('JENKINS_API_TOKEN')
    FLASK_SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key')
    BASIC_AUTH_USERNAME = os.getenv('BASIC_AUTH_USERNAME', 'admin')
    BASIC_AUTH_PASSWORD = os.getenv('BASIC_AUTH_PASSWORD', 'password')
```

---

### `app/__init__.py`

Creates and configures the Flask app instance:

```python
from flask import Flask
from dotenv import load_dotenv
import os

def create_app():
    app = Flask(__name__)
    load_dotenv()

    app.config.update({
        'BASIC_AUTH_USERNAME': os.getenv('BASIC_AUTH_USERNAME'),
        'BASIC_AUTH_PASSWORD': os.getenv('BASIC_AUTH_PASSWORD'),
        'SECRET_KEY': os.getenv('FLASK_SECRET_KEY'),
    })

    from app.routes import api
    app.register_blueprint(api)

    return app
```

---

### `app/routes.py`

Defines API endpoints:

* `/` — simple GET to verify API is running.
* `/trigger-job/<job_name>` — POST endpoint to trigger Jenkins job (protected by basic auth).
* `/health` — health check returning status.

Example route snippet:

```python
@api.route('/trigger-job/<job_name>', methods=['POST'])
@basic_auth_required
def trigger_job(job_name):
    parameters = request.get_json() or {}
    result = jenkins_service.trigger_job(job_name, parameters)

    if result['status'] == 'error':
        return jsonify(result), result.get('status_code', 500)
    return jsonify(result), result.get('status_code', 200)
```

---

### `app/utils/auth.py`

Provides `basic_auth_required` decorator that:

* Extracts `Authorization` header.
* Decodes base64 credentials.
* Compares with environment config.
* Returns `401 Unauthorized` if auth fails.

---

### `.env`

Contains sensitive configuration like Jenkins credentials and API user/password. **Not committed to repo.**

---

## Summary

This project demonstrates how to build a secure Flask API that triggers Jenkins jobs remotely. While simple in concept, challenges with networking in containerized or WSL environments and HTTP basic auth required careful debugging and setup.

If you run into issues connecting or authenticating:

* Confirm Flask app listens on `0.0.0.0`.
* Use the correct IP address depending on your environment (container, WSL, host).
* Double-check base64 encoding of `username:password`.
* Ensure environment variables are correctly loaded.

---

