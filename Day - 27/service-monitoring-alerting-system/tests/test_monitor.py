import pytest
from src.monitor import ServiceMonitor

class TestServiceMonitor:
    @pytest.fixture
    def sample_config(self):
        return {
            'service_url': 'https://httpbin.org/status/200',
            'check_interval': 1,
            'recipients': ['test@example.com'],
            'smtp': {
                'host': 'smtp.example.com',
                'port': 587,
                'sender': 'monitor@example.com'
            }
        }
    
    def test_service_check(self, sample_config):
        monitor = ServiceMonitor(sample_config)
        status, message = monitor.check_service()
        assert isinstance(status, bool)
        assert "Service is" in message
