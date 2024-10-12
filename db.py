import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

def create_problem(title, question, answer, difficulty):
    db = get_db()
    db.execute(
        'INSERT INTO PROBLEMS (TITLE, QUESTION, ANSWER, DIFFICULTY) VALUES (?, ?, ?, ?)',
        (title, question, answer, difficulty)
    )
    db.commit()  # Don't forget to commit changes

def get_problems():
    db = get_db()
    problems = db.execute('SELECT * FROM PROBLEMS').fetchall()
    return problems

# Function to create a new SQLite database
def create_database_table(db_name):
    conn = sqlite3.connect(db_name)
    # Example: Create a sample table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        );
    ''')
    conn.close()
