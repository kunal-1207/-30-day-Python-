# 🚀 Service Monitoring and Alerting System

![Python Version](https://img.shields.io/badge/python-3.6%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A robust Python solution for monitoring web service availability with email alerting capabilities.

## 🌟 Features

- **24/7 Service Monitoring**: Continuously checks HTTP/HTTPS endpoints
- **Smart Alerting**: Email notifications for both downtime and recovery
- **Retry Logic**: Automatic retries for flaky connections
- **Detailed Logging**: Console and file logging with timestamps
- **Configurable**: Easy YAML-based configuration

## 🛠 Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/service-monitoring-alerting-system.git
cd service-monitoring-alerting-system

# Create virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.\.venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt
```

## ⚙️ Configuration

1. Copy the example config file:
   ```bash
   cp config.example.yaml config.yaml
   ```

2. Edit `config.yaml` with your settings:

   ```yaml
   service:
     url: "https://example.com/health"  # Endpoint to monitor
     check_interval: 60                 # Seconds between checks
     max_retries: 3                     # Retry attempts
     retry_delay: 5                     # Seconds between retries
   
   email:
     recipients:
       - "admin@example.com"            # Alert recipients
     smtp:
       host: "smtp.example.com"         # SMTP server
       port: 587                        # SMTP port
       sender: "monitor@example.com"    # From address
       username: "your_username"        # SMTP credentials
       password: "your_password"
       tls: true                        # Enable TLS
   ```

## 🚦 Usage

### Basic Monitoring
```bash
python -m src.monitor
```

### Running as a Service
```bash
# Linux (systemd)
sudo cp service-monitor.service /etc/systemd/system/
sudo systemctl enable service-monitor
sudo systemctl start service-monitor
```

### Docker
```bash
docker build -t service-monitor .
docker run -d --name monitor service-monitor
```

## 📨 SMTP Setup Guide

### Popular Email Providers

| Provider       | SMTP Host          | Port  | TLS   |
|----------------|--------------------|-------|-------|
| Gmail          | smtp.gmail.com     | 587   | Yes   |
| Outlook/Hotmail| smtp.office365.com | 587   | Yes   |
| Yahoo          | smtp.mail.yahoo.com| 465   | SSL   |
| AWS SES        | email-smtp.us-west-2.amazonaws.com | 587 | Yes |

**Note:** For Gmail, you'll need to [create an App Password](https://myaccount.google.com/apppasswords) if using 2FA.

## 📊 Sample Alert Email

**Subject:** `ALERT: https://example.com/health is down`

```
Service https://example.com/health is unavailable.

First detected at: 2023-05-27 14:32:45
Error details: 503 Server Error: Service Unavailable
Consecutive failures: 3
```

## 🧪 Testing

Test with these endpoints:

```yaml
# Working endpoint
service_url: "https://httpbin.org/status/200"

# Failing endpoint
service_url: "https://httpbin.org/status/503"
```

Run unit tests:
```bash
pytest tests/
```

## 🐛 Troubleshooting

**Issue:** Emails not being delivered
- ✅ Verify SMTP credentials
- ✅ Check firewall allows outbound port 587
- ✅ Try with TLS disabled

**Issue:** False positives
- ✅ Increase `check_interval`
- ✅ Adjust `max_retries` and `retry_delay`

View logs:
```bash
tail -f logs/service_monitor.log
```

## 🤝 Contributing

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

## 📬 Contact

Project Link: [https://github.com/kunal-1207/service-monitoring-alerting-system](https://github.com/kunal-1207/30-day-Python-to-DevOps/tree/main/Day%20-%2027/service-monitoring-alerting-system)
