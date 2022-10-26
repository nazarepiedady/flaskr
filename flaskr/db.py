import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_database():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def close_database(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_database():
    db = get_database()

    with current_app.open_resource('schema.sql') as file:
        db.executescript(file.read().decode('utf8'))
