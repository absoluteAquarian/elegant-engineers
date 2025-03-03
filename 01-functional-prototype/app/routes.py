from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route('/')
def home():
    # Example list of (name, score) tuples
    scores = [
        ("Alice", 150),
        ("Bob", 120),
        ("Charlie", 100),
        ("David", 90),
        ("Eve", 80)
    ]
    return render_template('index.html', scores=scores)

@main.route('/about')
def about():
    return render_template('about.html')