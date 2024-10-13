import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext
from flask import Flask, request, redirect, url_for, render_template
import sqlite3
import os

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

   

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)



import sqlite3

def create_problem(table_name, question, answer, difficulty):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(f'''
            INSERT INTO {table_name} (question, answer, difficulty) VALUES (?, ?, ?)
        ''', (question, answer, difficulty))
        conn.commit()
    except Exception as e:
        print(f"Error inserting into {table_name}: {e}")
    finally:
        conn.close()

def get_db_connection():
    conn = sqlite3.connect('instance/app_database.db')
    conn.row_factory = sqlite3.Row  
    return conn

def get_all_tables():
    db = get_db()
    tables = db.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
    return [table['name'] for table in tables]
    
def get_all_questions():
    db = get_db()
    tables = db.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
    return [table['name'] for table in tables]

def get_problems_from_table(table_name):
    db = get_db()
    query = f'SELECT * FROM "{table_name}"'
    problems = db.execute(query).fetchall()

    
    return [dict(problem) for problem in problems]


app = Flask(__name__)

def create_database_table(t):
    title = t

    db_path = os.path.abspath('instance/app_database.db')
    print("Database path:", db_path)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

  
    table_name = title.replace(" ", "_").replace("-", "_")
    print("Creating table with name:", table_name)

    try:
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {table_name} (
                id INTEGER PRIMARY KEY,
                question TEXT NOT NULL,
                answer TEXT NOT NULL,
                difficulty TEXT NOT NULL
            )
        ''')
    except Exception as e:
        print("Error creating table:", e)

   
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Current tables:", tables)

    
    conn.commit()
    conn.close()

    return redirect(url_for('mq'))  
