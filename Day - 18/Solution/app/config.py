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
