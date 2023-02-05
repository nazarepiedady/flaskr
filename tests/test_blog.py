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
