from flask import Flask, render_template

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

@app.route('/create')
def create():
    return render_template('create.html')


if __name__ == '__main__':
    app.run(debug=True)
