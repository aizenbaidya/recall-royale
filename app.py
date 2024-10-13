from flask import Flask, render_template, request, redirect, url_for, g
import db
from db import create_problem, create_database_table, get_all_tables, get_problems_from_table, get_db

DIFFICULTY_EASY = 'easy'
DIFFICULTY_MEDIUM = 'medium'
DIFFICULTY_HARD = 'hard'


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
        global current_table_name 
        if not current_table_name:
            print("Table name not set!")
            return redirect(url_for('create'))

        print("THE CURRENT TABLE NAME: ", current_table_name, difficulty)

        questions, answers = extract_questions_and_answers(request.form)
        for question, answer in zip(questions, answers):
            create_problem(current_table_name, question, answer, difficulty)

    @app.route('/')
    def home():
        tables = get_all_tables()
        return render_template('home.html', tables=tables)

    @app.route('/create', methods=['GET', 'POST'])
    def create():
        global current_table_name

        if request.method == 'POST':
            title = request.form['title']
            current_table_name = title.replace(" ", "_").replace("-", "_")
            create_database_table(title) 
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
        subject = request.args.get('subject')
        db = get_db()
        if subject:  
            try:
                query = f"SELECT question FROM {subject}"
                results = db.execute(query).fetchall()  
                problems = [row[0] for row in results] 

                query2 = f"SELECT answer FROM {subject}"
                results2 = db.execute(query2).fetchall()
                answers = [row[0] for row in results2]

            except Exception as e:
                return f"Error accessing table {subject}: {e}"
            
            return render_template('play.html', subject=subject, problems=problems, answers=answers)
        else:
            return "No subject selected!"
    
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
                    'question': problem['question'],
                    'answer': problem['answer'],
                    'difficulty': problem['difficulty']
                }
                for problem in problems
            ]
        
        return render_template('problems.html', problems_by_table=problems_by_table)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
