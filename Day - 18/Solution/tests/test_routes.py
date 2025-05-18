import unittest
from app import create_app
import os

class TestJenkinsAPI(unittest.TestCase):
    def setUp(self):
        os.environ['BASIC_AUTH_USERNAME'] = 'test'
        os.environ['BASIC_AUTH_PASSWORD'] = 'test'
        self.app = create_app()
        self.client = self.app.test_client()
        self.auth = ('test', 'test')

    def test_health_check(self):
        response = self.client.get('/api/health')
        self.assertEqual(response.status_code, 200)

    def test_trigger_job_unauthorized(self):
        response = self.client.post('/api/trigger-job/test-job')
        self.assertEqual(response.status_code, 401)

    def test_trigger_job_authorized(self):
        response = self.client.post(
            '/api/trigger-job/test-job',
            headers={'Authorization': 'Basic ' + 
                   'dGVzdDp0ZXN0'.encode('utf-8').decode('utf-8')}
        )
        # This will likely fail with 404 unless you have a real Jenkins server
        # We're just testing the auth flow here
        self.assertIn(response.status_code, [404, 500])

if __name__ == '__main__':
    unittest.main()
