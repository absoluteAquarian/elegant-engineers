from flask import Flask, request, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database connection function
def get_db_connection():
    conn = sqlite3.connect('leaderboard.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    # Fetch the top 10 users from the leaderboard
    conn = get_db_connection()
    leaderboard = conn.execute('''
        SELECT User.userName, Leaderboard.userRank, Leaderboard.userTopRank
        FROM Leaderboard
        JOIN User ON Leaderboard.userId = User.userId
        ORDER BY Leaderboard.userRank ASC
        LIMIT 10''').fetchall()
    conn.close()
    return render_template('index.html', leaderboard=leaderboard)

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        user_name = request.form['username']
        conn = get_db_connection()
        conn.execute('INSERT INTO User (userName) VALUES (?)', (user_name,))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add_user.html')

@app.route('/add_score/<int:user_id>', methods=['GET', 'POST'])
def add_score(user_id):
    if request.method == 'POST':
        score = request.form['score']
        conn = get_db_connection()

        # Insert score
        conn.execute('INSERT INTO Score (score, userId) VALUES (?, ?)', (score, user_id))
        conn.commit()

        # Update leaderboard (This could be more complex with ranking logic)
        conn.execute('UPDATE Leaderboard SET userRank = userRank + 1 WHERE userId = ?', (user_id,))
        conn.commit()

        conn.close()
        return redirect(url_for('index'))

    return render_template('add_score.html', user_id=user_id)

@app.route('/leaderboard')
def leaderboard():
    # Fetch the leaderboard entries
    conn = get_db_connection()
    leaderboard = conn.execute('''
        SELECT User.userName, Score.score, Score.dateSubmitted
        FROM Score
        JOIN User ON Score.userId = User.userId
        ORDER BY Score.score DESC''').fetchall()
    conn.close()
    return render_template('leaderboard.html', leaderboard=leaderboard)

if __name__ == '__main__':
    app.run(debug=True)
