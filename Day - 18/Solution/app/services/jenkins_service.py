import requests
from requests.auth import HTTPBasicAuth
from app.config import Config
import logging

logger = logging.getLogger(__name__)

class JenkinsService:
    def __init__(self):
        self.jenkins_url = Config.JENKINS_URL
        self.auth = HTTPBasicAuth(Config.JENKINS_USERNAME, Config.JENKINS_API_TOKEN)

    def trigger_job(self, job_name, parameters=None):
        """
        Trigger a Jenkins job with optional parameters
        
        Args:
            job_name (str): Name of the Jenkins job
            parameters (dict): Job parameters (optional)
            
        Returns:
            dict: Response from Jenkins API
        """
        try:
            # Check if job exists first
            job_url = f"{self.jenkins_url}/job/{job_name}/api/json"
            response = requests.get(job_url, auth=self.auth)
            
            if response.status_code != 200:
                return {
                    'status': 'error',
                    'message': f'Job {job_name} not found or access denied',
                    'status_code': response.status_code
                }

            # Build URL depends on whether we have parameters or not
            if parameters:
                build_url = f"{self.jenkins_url}/job/{job_name}/buildWithParameters"
                response = requests.post(build_url, auth=self.auth, params=parameters)
            else:
                build_url = f"{self.jenkins_url}/job/{job_name}/build"
                response = requests.post(build_url, auth=self.auth)

            if response.status_code in [200, 201]:
                queue_location = response.headers.get('Location')
                return {
                    'status': 'success',
                    'message': f'Job {job_name} triggered successfully',
                    'queue_location': queue_location,
                    'status_code': response.status_code
                }
            else:
                logger.error(f"Failed to trigger job {job_name}. Status code: {response.status_code}")
                return {
                    'status': 'error',
                    'message': f'Failed to trigger job {job_name}',
                    'status_code': response.status_code
                }

        except requests.exceptions.RequestException as e:
            logger.error(f"Error triggering Jenkins job: {str(e)}")
            return {
                'status': 'error',
                'message': f'Error connecting to Jenkins: {str(e)}',
                'status_code': 500
            }
