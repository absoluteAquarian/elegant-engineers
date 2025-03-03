from flask import Flask
from .config import Config
from .models import db
from .routes import main

def create_app(config_filename='config.py'):
    app = Flask(__name__)
    app.config.from_object(Config)  # Default config
    app.config.from_pyfile(config_filename)  # Load instance config

    db.init_app(app)

    app.register_blueprint(main)

    return app