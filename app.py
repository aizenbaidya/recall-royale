from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

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

@app.route('/create', methods=['GET', 'POST'])  # Allow GET and POST methods
def create():
    if request.method == 'POST':
        # Handle the form data for creating the questions
        # Here you can process the title or other inputs if needed

        # Redirect to the mq page after creating
        return redirect(url_for('mq'))  # Redirect to /mq
    
    return render_template('create.html')  # Render template for GET requests

@app.route('/mq', methods=['GET', 'POST'])  # Allow GET and POST methods
def mq():
    if request.method == 'POST':
        # Handle the form data
        title = request.form['title']
        questions = []
        answers = []
        
        # Loop through questions and answers
        for i in range(1, (len(request.form) // 2) + 1):  
            questions.append(request.form.get(f'question{i}'))
            answers.append(request.form.get(f'answer{i}'))
        
        # Process the data (e.g., save to database)
        print("Title:", title)
        print("Questions:", questions)
        print("Answers:", answers)
        
        # Redirect to the HQ route after processing
        return redirect(url_for('mq'))  # Change this to redirect to /hq
        
    return render_template('mq.html')  # Render template for GET requests

@app.route('/hq', methods=['GET', 'POST'])  # Allow GET and POST methods
def hq():
    if request.method == 'POST':
        # Handle the form data
        title = request.form['title']
        questions = []
        answers = []
        
        # Loop through questions and answers
        for i in range(1, (len(request.form) // 2) + 1):  
            questions.append(request.form.get(f'question{i}'))
            answers.append(request.form.get(f'answer{i}'))
        
        # Process the data (e.g., save to database)
        print("Title:", title)
        print("Questions:", questions)
        print("Answers:", answers)
        
        # Redirect to some route after processing (adjust if needed)
        return redirect(url_for('hq'))  # Redirect to /play after submitting HQ
    
    return render_template('hq.html')  # Render template for GET requests

if __name__ == '__main__':
    app.run(debug=True)