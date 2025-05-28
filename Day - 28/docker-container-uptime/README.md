# Docker Container Uptime Monitor

A Python script that lists all running Docker containers and logs their uptime using the Docker SDK.

## Features

- Lists all running Docker containers
- Calculates and displays container uptime in human-readable format
- Logs container information including:
  - Container ID
  - Name
  - Image
  - Status
  - Uptime
- Comprehensive error handling
- Logs output to both console and file (`container_uptime.log`)

## Prerequisites

- Docker installed and running
- Python 3.6 or higher
- Docker SDK for Python

## Installation

1. Clone this repository or download the script:
   ```bash
   git clone [your-repo-url]
   cd [your-repo-directory]
   ```

2. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install the required package:
   ```bash
   pip install docker
   ```

## Usage

Run the script directly:
```bash
python docker_uptime_logger.py
```

### Expected Output
The script will display output in the console and write to `container_uptime.log`:
```
2023-05-28 14:30:00,123 - INFO - Found 3 running containers:
2023-05-28 14:30:00,124 - INFO - Container ID: a1b2c3d, Name: web-server, Image: nginx:latest, Status: running, Uptime: 2d 4h 30m 15s
2023-05-28 14:30:00,125 - INFO - Container ID: e4f5g6h, Name: db, Image: postgres:13, Status: running, Uptime: 1d 12h 45m 22s
```

## Configuration

You can modify the logging behavior by editing these parts of the script:

```python
logging.basicConfig(
    level=logging.INFO,  # Change to DEBUG for more verbose output
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('container_uptime.log'),  # Change log file name
        logging.StreamHandler(sys.stdout)
    ]
)
```

## Scheduling Regular Runs (Optional)

To run this script periodically (e.g., every hour), you can:

### On Linux/macOS:
Add to crontab:
```bash
0 * * * * /path/to/your/venv/python /path/to/docker_uptime_logger.py
```

### On Windows:
Use Task Scheduler to create a basic task that runs hourly.

## Troubleshooting

### Common Issues:
1. **Docker connection errors**:
   - Ensure Docker daemon is running
   - Verify your user has permission to access Docker

2. **Module not found errors**:
   - Confirm you installed the package in the correct virtual environment
   - Run `pip install docker` again if needed

3. **Permission denied errors**:
   - On Linux/macOS, add your user to the docker group:
     ```bash
     sudo usermod -aG docker $USER
     ```

## License

This project is open source and available under the [MIT License](LICENSE).

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements.
