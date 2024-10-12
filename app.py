from flask import Flask, render_template, request, redirect, url_for
import db  # Import the db module
from db import create_problem, get_problems

# Constants for problem difficulty
DIFFICULTY_EASY = 'easy'
DIFFICULTY_MEDIUM = 'medium'
DIFFICULTY_HARD = 'hard'

# Constants for titles
TITLE_MEDIUM = 'MEDIUM problems'
TITLE_HARD = 'HARD problems'


def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        DATABASE="instance/problems.sqlite",  # Ensure the path is correct
    )

    # Initialize the database
    db.init_app(app)

    # Utility function to extract questions and answers from the form
    def extract_questions_and_answers(form):
        questions = []
        answers = []
        for i in range(1, (len(form) // 2) + 1):
            questions.append(form.get(f'question{i}'))
            answers.append(form.get(f'answer{i}'))
        return questions, answers

    # Utility function to handle problem creation
    def create_problems(title, difficulty):
        questions, answers = extract_questions_and_answers(request.form)
        for question, answer in zip(questions, answers):
            create_problem(title, question, answer, difficulty)

    @app.route('/')
    def home():
        return render_template('home.html')

    @app.route('/about')
    def about():
        return render_template('about.html')

    @app.route('/play')
    def play():
        return render_template('play.html')

    @app.route('/tutorial')
    def tutorial():
        return render_template('tutorial.html')

    @app.route('/create', methods=['GET', 'POST'])
    def create():
        if request.method == 'POST':
            title = request.form['title']
            # Assuming you want to handle easy problems here
            create_problems(title, DIFFICULTY_EASY)
            return redirect(url_for('mq'))  # Redirect to /mq after creation
        return render_template('create.html')

    @app.route('/mq', methods=['GET', 'POST'])
    def mq():
        if request.method == 'POST':
            create_problems(TITLE_MEDIUM, DIFFICULTY_MEDIUM)
            return redirect(url_for('hq'))  # Redirect after processing
        return render_template('mq.html')  # Render template for GET request

    @app.route('/hq', methods=['GET', 'POST'])
    def hq():
        if request.method == 'POST':
            create_problems(TITLE_HARD, DIFFICULTY_HARD)
            return redirect(url_for('problems'))  # Redirect after processing
        return render_template('hq.html')  # Render template for GET requests

    # Route for displaying problems
    @app.route('/problems')
    def problems():
        problems = get_problems()  # Fetch problems from the database
        return render_template('problems.html', problems=problems)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
