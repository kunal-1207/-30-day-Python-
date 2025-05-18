from flask import Flask
from dotenv import load_dotenv
import os

def create_app():
    app = Flask(__name__)
    load_dotenv()

    # Configuration
    app.config.update({
        'BASIC_AUTH_USERNAME': os.getenv('BASIC_AUTH_USERNAME'),
        'BASIC_AUTH_PASSWORD': os.getenv('BASIC_AUTH_PASSWORD'),
        'SECRET_KEY': os.getenv('FLASK_SECRET_KEY'),
        # Remove BASIC_AUTH_FORCE because you do manual auth decorator
    })

    # Import and register blueprints
    from app.routes import api  # Make sure this matches the blueprint name
    app.register_blueprint(api)  # No url_prefix needed if root

    return app
