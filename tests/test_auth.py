import pytest
from flask import g, session
from flaskr.db import get_database


def test_register(client, application):
    ''' test the register '''
    login_route_path = '/auth/login'
    register_route_path = '/auth/register'
    user = {'username': 'a', 'password': 'a'}
    response = client.post(register_route_path, data=user)

    assert client.get(register_route_path).status_code == 200
    assert response.headers['Location'] == '/auth/login'

    with application.app_context():
        assert get_database().execute(
            "SELECT * FROM user WHERE username = 'a'",
        ).fetchone() is not None

@pytest.mark.parametrize(('username', 'password', 'message'),(
    ('', '', b'Username is required.'),
    ('a', '', b'Password is required.'),
    ('test', 'test', b'already registered'),
))
def test_register_validate_input(client, username, password, message):
    ''' test the register validade input '''
    response = client.post(
        '/auth/register',
        data={'username': username, 'password': password}
    )
    assert message in response.data

def test_login(client, authentication):
    ''' test the login '''
    response = authentication.login()
    assert client.get('/auth/login').status_code == 200
    assert response.headers['Location'] == '/'

    with client:
        client.get('/')
        assert session['user_id'] == 1
        assert g.user['username'] == 'test'
