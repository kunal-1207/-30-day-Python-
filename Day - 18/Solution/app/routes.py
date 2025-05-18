from flask import Blueprint, request, jsonify
from app.services.jenkins_service import JenkinsService
from app.utils.auth import basic_auth_required

api = Blueprint('api', __name__)
jenkins_service = JenkinsService()

@api.route('/', methods=['GET'])
def index():
    return 'Jenkins Trigger API is running.', 200

@api.route('/trigger-job/<job_name>', methods=['POST'])
@basic_auth_required
def trigger_job(job_name):
    """
    Trigger a Jenkins job
    ---
    parameters:
      - name: job_name
        in: path
        type: string
        required: true
      - name: parameters
        in: body
        schema:
          type: object
          properties:
            param1:
              type: string
            param2:
              type: string
    responses:
      200:
        description: Job triggered successfully
      401:
        description: Unauthorized
      404:
        description: Job not found
      500:
        description: Internal server error
    """
    parameters = request.get_json() or {}

    result = jenkins_service.trigger_job(job_name, parameters)

    if result['status'] == 'error':
        return jsonify(result), result.get('status_code', 500)

    return jsonify(result), result.get('status_code', 200)

@api.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint
    ---
    responses:
      200:
        description: API is healthy
    """
    return jsonify({'status': 'healthy'}), 200
