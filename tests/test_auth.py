import pytest
from flask import g, session
from flaskr.db import get_database


def test_register(client, application):
    ''' test the register route path '''
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
