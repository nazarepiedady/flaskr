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
