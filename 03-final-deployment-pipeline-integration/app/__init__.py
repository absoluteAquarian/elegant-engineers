from flask import Flask
from .config import Config
from .models import db
from .routes import main
from dotenv import load_dotenv

# import os
import cloudinary

cloudinary.config(
    # os.getenv() works on local builds, but not deployment?
    cloud_name='dtrhkewms',
    api_key='377774626274684',
    api_secret='KrsCIkhslhELZua8em7wTAIoxSE'
)

load_dotenv()


def create_app(config_filename='config.py'):
    app = Flask(__name__)
    app.config.from_object(Config)  # Default config
    app.config.from_pyfile(config_filename)  # Load instance config

    app.config['IMGUR_CLIENT_ID'] = 'c6f459f46dce695'

    db.init_app(app)

    # Create database tables
    with app.app_context():
        db.create_all()
        db.session.commit()

    app.register_blueprint(main)

    return app
