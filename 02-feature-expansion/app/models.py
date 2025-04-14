from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Define the Score model
class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    dateSubmitted = db.Column(db.DateTime, nullable=False)
    imageUrl = db.Column(db.String(255), nullable=True)

class Leaderboard(db.Model):
    userId = db.Column(db.Integer, primary_key=True)
    userRank = db.Column(db.Integer, nullable=False)
    userTopRank = db.Column(db.Integer, nullable=False)

class User(db.Model):
    userId = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String(50), nullable=False)