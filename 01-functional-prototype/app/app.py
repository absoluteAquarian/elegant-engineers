from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///leaderboard.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the Score model
class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    score = db.Column(db.Integer, nullable=False)

# Create database tables
with app.app_context():
    db.create_all()

### ROUTES ###

# Home route (Leaderboard Page)
@app.route('/')
def leaderboard():
    scores = Score.query.order_by(Score.score.desc()).limit(10).all()
    return render_template('leaderboard.html', scores=scores)

# Submit Score Page
@app.route('/submit', methods=['GET'])
def submit_form():
    return render_template('submit.html')

# Handle Score Submission (Form)
@app.route('/submit', methods=['POST'])
def submit_score():
    name = request.form.get('name')
    score = request.form.get('score')

    if name and score:
        new_score = Score(name=name, score=int(score))
        db.session.add(new_score)
        db.session.commit()
    
    return redirect(url_for('leaderboard'))

# API: Get Scores
@app.route('/api/scores', methods=['GET'])
def get_scores():
    scores = Score.query.order_by(Score.score.desc()).limit(10).all()
    scores_list = [{"name": s.name, "score": s.score} for s in scores]
    return jsonify({"scores": scores_list})

# API: Submit Score via JSON
@app.route('/api/scores', methods=['POST'])
def add_score():
    data = request.get_json()
    name = data.get("name")
    score = data.get("score")

    if not name or not score:
        return jsonify({"success": False, "message": "Invalid data"}), 400

    new_score = Score(name=name, score=int(score))
    db.session.add(new_score)
    db.session.commit()
    
    return jsonify({"success": True, "message": "Score added!"})
