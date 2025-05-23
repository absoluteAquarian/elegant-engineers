from flask import Flask, Blueprint, request, jsonify, render_template, redirect, url_for
import sqlite3
from .models import Score, db, User
from datetime import datetime
from sqlalchemy import text

main = Blueprint('main', __name__)

# Database connection function
def get_db_connection():
#    conn = sqlite3.connect('leaderboard.db')
#    conn.row_factory = sqlite3.Row
#    return conn
    return db.session


# Submit Score Page
@main.route('/submit', methods=['GET'])
def submit_form():
    return render_template('submit.html')


# Handle Score Submission (Form)
@main.route('/submit', methods=['POST'])
def submit_score():
    name = request.form.get('name')
    score = request.form.get('score')

    if name and score:
        new_score = Score(name=name, score=int(score), dateSubmitted=datetime.utcnow())
        db.session.add(new_score)
        db.session.commit()
        return redirect(url_for('main.leaderboard'))

    return redirect(url_for('main.submit_form'))


# API: Get Scores
@main.route('/api/scores', methods=['GET'])
def get_scores():
    scores = Score.query.order_by(Score.score.desc()).limit(10).all()
    scores_list = [{"name": s.name, "score": s.score} for s in scores]
    return jsonify({"scores": scores_list})


# API: Submit Score via JSON
@main.route('/api/scores', methods=['POST'])
def add_score():
    data = request.get_json()
    name = data.get("name")
    score = data.get("score")

    if not name or not score:
        return jsonify({"success": False, "message": "Invalid data"}), 400

    new_score = Score(name=name, score=int(score), dateSubmitted=datetime.utcnow())
    db.session.add(new_score)
    db.session.commit()

    return jsonify({"success": True, "message": "Score added!"})

@main.route('/')
def index():
    conn = get_db_connection()

    # Fetch the top 10 users from the leaderboard
    board = conn.execute(text('''
        SELECT user.userName, leaderboard.userRank, leaderboard.userTopRank
        FROM leaderboard
        JOIN user ON leaderboard.userId = user.userId
        ORDER BY leaderboard.userRank ASC
        LIMIT 10''')).fetchall()
    conn.close()
    return render_template('index.html', scores=board)

@main.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        user_name = request.form['username']
        conn = get_db_connection()
        conn.execute(text('INSERT INTO user (userName) VALUES (:name)'), {'name': user_name})
        conn.commit()
        conn.close()
        return redirect(url_for('main.index'))
    return render_template('add_user.html')

@main.route('/leaderboard')
def leaderboard():
    # Fetch the leaderboard entries
    conn = get_db_connection()
    board = conn.execute(text('''
        SELECT score.name, score.score, score.dateSubmitted
        FROM score
        ORDER BY score.score DESC''')).fetchall()
    conn.close()
    return render_template('leaderboard.html', leaderboard_scores=board)