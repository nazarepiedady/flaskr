import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_database():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DETECT_TYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def close_database():
    db = g.pop('db', None)

    if db is not None:
        db.close()
