# Service Monitoring and Alerting System

A Python-based solution to monitor service uptime and send email alerts during downtime.

## Features

- 🕵️‍♂️ Continuous service monitoring with configurable intervals
- 📧 Email alerts for service downtime and recovery
- 🔄 Automatic retries for both service checks and email sending
- 📊 Tracks consecutive failures and downtime duration
- 📝 Detailed logging to console and file

## Prerequisites

- Python 3.6+
- Required packages: `requests`, `retry`

## Installation

1. Clone the repository or download the script
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install requests retry
   ```

## Configuration

Edit the configuration in the `__main__` section of the script:

```python
config = {
    'service_url': 'https://your-service.com/health',  # URL to monitor
    'check_interval': 60,  # Check interval in seconds
    'recipients': ['admin@example.com'],  # List of recipient emails
    'smtp': {
        'host': 'smtp.example.com',      # SMTP server
        'port': 587,                     # SMTP port
        'sender': 'monitor@example.com',  # From address
        'username': 'your_username',     # SMTP username
        'password': 'your_password',     # SMTP password
        'tls': True                      # Use TLS (True/False)
    }
}
```

## Running the Monitor

Execute the script:
```bash
python smtp.py
```

The script will:
1. Create a log file `service_monitor.log`
2. Begin monitoring the specified URL
3. Send alerts when the service goes down or recovers

## Testing

For testing purposes, you can use these endpoints:

- Working endpoint: `https://httpbin.org/status/200`
- Failing endpoint: `https://httpbin.org/status/500`

## SMTP Configuration Guide

### For Gmail Users:
1. Use these SMTP settings:
   ```python
   'host': 'smtp.gmail.com',
   'port': 587,
   'tls': True
   ```
2. Create an App Password:
   - Go to your Google Account > Security
   - Enable 2-Step Verification
   - Generate an App Password for mail

### For Other Providers:
Check your email provider's SMTP documentation for the correct settings.

## Logging

The system logs to both console and `service_monitor.log` with timestamps. Log levels:
- INFO: Normal operation messages
- WARNING: Service check failures
- ERROR: Critical failures

## Stopping the Monitor

Press `Ctrl+C` to stop the monitoring process gracefully.

## Customization Options

1. Add more recipients to the `recipients` list
2. Adjust `check_interval` for more/less frequent checks
3. Modify retry parameters in the `@retry` decorators
4. Add additional health check criteria

## Troubleshooting

**Service checks fail immediately:**
- Verify the URL is correct and accessible
- Check your network connection

**Email alerts not sending:**
- Verify SMTP credentials
- Check for firewall blocking port 587
- Try with TLS disabled if your provider doesn't support it

**Too many alerts:**
- Increase the `check_interval`
- Adjust the retry parameters in the `check_service` method

## License

This project is open-source and available under the MIT License.
