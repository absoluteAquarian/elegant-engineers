from flask import Blueprint, render_template

main = Blueprint('main', __name__)


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