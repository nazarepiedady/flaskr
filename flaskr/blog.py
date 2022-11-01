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


@blueprint.route('/create')
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            database = get_database()
            database.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            database.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')


def get_post(id, check_author=True):
    post = get_database().execute(
        'SELECT post.id, title, body, created, author_id, username'
        ' WHERE post.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f'Post id {id} does not exist.')

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post


@blueprint.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            database = get_database()
            database.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            database.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)


@blueprint.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    database = get_database()
    database.execute('DELETE FROM post WHERE id = ?', (id,))
    database.commit()
    return redirect(url_for('blog.index'))
