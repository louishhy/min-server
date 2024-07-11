# An application factory pattern that helps you create app.
from flask import Flask
from .routes import register_routes
from app import config

def create_app(config_class=config.Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initializing extensions
    
    # Register routes w/ blueprints
    register_routes(app)

    return app