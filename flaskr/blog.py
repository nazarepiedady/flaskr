from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_database


blueprint = Blueprint('blog', __name__)


@blueprint.route('/')
def index():
    database = get_database()
    posts = database.execute(
        'SELECT post.id, title, body, created, author_id, username'
        ' FROM post JOIN user ON post.author_id = user.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('blog/index.html', posts=posts)
