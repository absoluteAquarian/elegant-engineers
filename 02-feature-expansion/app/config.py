import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'default_secret_key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///leaderboard.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
     IMGUR_CLIENT_ID = os.getenv('c6f459f46dce695')