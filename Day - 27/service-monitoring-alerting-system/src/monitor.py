import smtplib
import time
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from retry import retry
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('service_monitor.log'),
        logging.StreamHandler()
    ]
)

class ServiceMonitor:
    def __init__(self, config):
        self.service_url = config['service_url']
        self.check_interval = config.get('check_interval', 60)
        self.max_retries = config.get('max_retries', 3)
        self.retry_delay = config.get('retry_delay', 5)
        
        # Email configuration
        self.smtp_config = config['smtp']
        self.recipients = config['recipients']
        
        # State tracking
        self.last_status = None
        self.downtime_start = None
        self.consecutive_failures = 0
        
        # Validate config
        self._validate_config()

    def _validate_config(self):
        """Validate the configuration"""
        if not self.service_url.startswith(('http://', 'https://')):
            raise ValueError("service_url must start with http:// or https://")
        if not isinstance(self.recipients, list) or len(self.recipients) == 0:
            raise ValueError("recipients must be a non-empty list")
        
    @retry(tries=3, delay=2, backoff=2, logger=logging)
    def check_service(self):
        """Check the service status with retry logic"""
        try:
            response = requests.get(
                self.service_url,
                timeout=10,
                headers={'User-Agent': 'ServiceMonitor/1.0'}
            )
            response.raise_for_status()
            return True, f"Service is UP. Status code: {response.status_code}"
        except requests.exceptions.RequestException as e:
            logging.warning(f"Service check failed: {str(e)}")
            return False, f"Service is DOWN. Error: {str(e)}"
    
    @retry(tries=3, delay=5, jitter=(1, 3), logger=logging)
    def send_alert(self, subject, body):
        """Send email alert with retry logic"""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.smtp_config['sender']
            msg['To'] = ', '.join(self.recipients)
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'plain'))
            
            with smtplib.SMTP(
                host=self.smtp_config['host'],
                port=self.smtp_config['port']
            ) as server:
                if self.smtp_config.get('tls', False):
                    server.starttls()
                if self.smtp_config.get('username'):
                    server.login(
                        self.smtp_config['username'],
                        self.smtp_config['password']
                    )
                server.sendmail(
                    self.smtp_config['sender'],
                    self.recipients,
                    msg.as_string()
                )
            logging.info(f"Alert sent: {subject}")
            return True
        except smtplib.SMTPException as e:
            logging.error(f"Failed to send alert: {str(e)}")
            raise
    
    def monitor(self):
        """Main monitoring loop"""
        logging.info(f"Starting service monitor for {self.service_url}")
        
        try:
            while True:
                try:
                    current_status, message = self.check_service()
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    logging.info(f"{message}")
                    
                    # Track consecutive failures
                    if current_status:
                        self.consecutive_failures = 0
                    else:
                        self.consecutive_failures += 1
                    
                    # Detect status change
                    if self.last_status is None:
                        self.last_status = current_status
                    elif current_status != self.last_status:
                        if current_status:  # Service recovered
                            if self.downtime_start:
                                downtime_duration = datetime.now() - self.downtime_start
                                alert_subject = f"RECOVERED: {self.service_url} is back online"
                                alert_body = (
                                    f"Service {self.service_url} has recovered.\n"
                                    f"Downtime duration: {str(downtime_duration)}\n"
                                    f"Recovery time: {timestamp}"
                                )
                                self.send_alert(alert_subject, alert_body)
                                self.downtime_start = None
                        else:  # Service went down
                            self.downtime_start = datetime.now()
                            alert_subject = f"ALERT: {self.service_url} is down"
                            alert_body = (
                                f"Service {self.service_url} is unavailable.\n"
                                f"First detected at: {timestamp}\n"
                                f"Error details: {message.split(':')[-1].strip()}\n"
                                f"Consecutive failures: {self.consecutive_failures}"
                            )
                            self.send_alert(alert_subject, alert_body)
                        
                        self.last_status = current_status
                    
                    time.sleep(self.check_interval)
                
                except KeyboardInterrupt:
                    logging.info("Monitoring stopped by user")
                    raise
                except Exception as e:
                    logging.error(f"Unexpected error in monitoring loop: {str(e)}")
                    time.sleep(min(60, self.check_interval))  # Wait before retrying
        
        except KeyboardInterrupt:
            logging.info("Service monitor stopped")
            return

if __name__ == "__main__":
    # Test configuration - REPLACE WITH YOUR ACTUAL VALUES
    config = {
        'service_url': 'https://httpbin.org/status/200',  # Test with a reliable endpoint
        'check_interval': 30,  # seconds
        'recipients': ['recipient.emai@gmail.com'],
        'smtp': {
            'host': 'smtp.gmail.com',  # Example for Gmail
            'port': 587,
            'sender': 'your.email@gmail.com',
            'username': 'your.email@gmail.com',
            'password': 'your_app_password',  # Use app-specific password
            'tls': True
        }
    }
    
    try:
        monitor = ServiceMonitor(config)
        monitor.monitor()
    except Exception as e:
        logging.error(f"Failed to start monitor: {str(e)}")
