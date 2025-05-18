from functools import wraps
from flask import request, jsonify
from app.config import Config

def basic_auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not (auth.username == Config.BASIC_AUTH_USERNAME and auth.password == Config.BASIC_AUTH_PASSWORD):
            return jsonify({
                'status': 'error',
                'message': 'Basic authentication required'
            }), 401
        return f(*args, **kwargs)
    return decorated
