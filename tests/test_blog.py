import pytest
from flaskr.db import get_database


def test_index(client, authentication):
    ''' test the index route '''
    response = client.get('/')
    assert b'Log In' in response.data
    assert b'Register' in response.data

    authentication.login()
    response = client.get('/')
    assert b'Log Out' in response.data
    assert b'test title' in response.data
    assert b'by test on 2018-01-01' in response.data
    assert b'test\nbody' in response.data
    assert b'href="/1/update"' in response.data

@pytest.mark.parametrize('path', (
    '/create',
    '/1/update',
    '/1/delete'
))
def test_login_required(client, path):
    response = client.post(path)
    assert response.headers['Location'] == '/auth/login'

def test_author_required(application, client, authentication):
    # change the post author to another user
    with application.app_context():
        database = get_database()
        database.execute('UPDATE post SET author_id = 2 WHERE id = 1')
        database.commit()

    authentication.login()
    # current user can't modify other user's post
    assert client.post('/1/update').status_code == 403
    assert client.post('/1/delete').status_code == 403
    # current user doesn't see edit link
    assert b'href="/1/update"' not in client.get('/').data

@pytest.mark.parametrize('path', (
    '/2/update',
    '/2/delete',
))
def test_exists_required(client, authentication, path):
    authentication.login()
    assert client.post(path).status_code == 404

def test_create(client, authentication, application):
    authentication.login()
    assert client.get('/create').status_code == 200
    client.post('/create', data={'title': 'created', 'body': ''})

    with application.app_context():
        database = get_database()
        count = database.execute('SELECT COUNT(id) FROM post').fetchone()[0]
        assert count == 2

def test_update(client, authentication, application):
    authentication.login()
    assert client.get('/1/update').status_code == 200
    client.post('/1/update', data={'title': 'updated', 'body': ''})

    with application.app_context():
        database = get_database()
        post = database.execute('SELECT * FROM post WHERE id = 1').fetchone()
        assert post['title'] == 'updated'

@pytest.mark.parametrize('path', (
    '/create',
    '/1/update',
))
def test_create_update_validate(client, authentication, path):
    authentication.login()
    response = client.post(path, data={'title': '', 'body': ''})
    assert b'Title is required.' in response.data
