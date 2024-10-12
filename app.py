from flask import Flask, render_template, request, redirect, url_for, g
import db
from db import create_problem, create_database_table, get_all_tables, get_problems_from_table

DIFFICULTY_EASY = 'easy'
DIFFICULTY_MEDIUM = 'medium'
DIFFICULTY_HARD = 'hard'

# Global variable to store the table name
current_table_name = None

def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        DATABASE="instance/app_database.db",
    )

    db.init_app(app)

    def extract_questions_and_answers(form):
        questions = []
        answers = []
        for i in range(1, (len(form) // 2) + 1):
            questions.append(form.get(f'question{i}'))
            answers.append(form.get(f'answer{i}'))
        return questions, answers

    def create_problems(difficulty):
        global current_table_name  # Use the global variable

        if not current_table_name:
            print("Table name not set!")
            return redirect(url_for('create'))

        print("THE CURRENT TABLE NAME: ", current_table_name, difficulty)

        questions, answers = extract_questions_and_answers(request.form)
        for question, answer in zip(questions, answers):
            create_problem(current_table_name, question, answer, difficulty)

    @app.route('/')
    def home():
        return render_template('home.html')

    @app.route('/create', methods=['GET', 'POST'])
    def create():
        global current_table_name  # Declare the global variable

        if request.method == 'POST':
            title = request.form['title']
            current_table_name = title.replace(" ", "_").replace("-", "_")  # Set the global variable for the current table
            create_database_table(title)  # Create the database table
            create_problems(DIFFICULTY_EASY)

            return redirect(url_for('mq'))

        return render_template('create.html')

    @app.route('/mq', methods=['GET', 'POST'])
    def mq():
        if request.method == 'POST':
            create_problems(DIFFICULTY_MEDIUM)
            return redirect(url_for('hq'))

        return render_template('mq.html')

    @app.route('/hq', methods=['GET', 'POST'])
    def hq():
        if request.method == 'POST':
            create_problems(DIFFICULTY_HARD)
            return redirect(url_for('problems'))

        return render_template('hq.html')

    @app.route('/play')
    def play():
        return render_template('play.html') 

    @app.route('/tutorial')
    def tutorial():
        return render_template('tutorial.html') 
    
    @app.route('/about')
    def about():
        return render_template('about.html')
    
    @app.route('/problems')
    def problems():
        tables = get_all_tables()
        problems_by_table = {}
        
        for table in tables:
            problems = get_problems_from_table(table)
            problems_by_table[table] = [
                {
                    'question': problem['QUESTION'],
                    'answer': problem['ANSWER'],
                    'difficulty': problem['DIFFICULTY']
                }
                for problem in problems
            ]
        
        return render_template('problems.html', problems_by_table=problems_by_table)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
