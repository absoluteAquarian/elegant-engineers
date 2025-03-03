from flask import Flask
from .models import db
from .routes import main

def create_app(config_filename='config.py'):
    app = Flask(__name__)
    app.config.from_pyfile(config_filename)

    db.init_app(app)

    app.register_blueprint(main)

    return app