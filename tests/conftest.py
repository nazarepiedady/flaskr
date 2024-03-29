import os
import tempfile

import pytest
from flaskr import create_app
from flaskr.db import get_database, init_database


with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as file:
    _data_sql = file.read().decode('utf-8')


@pytest.fixture
def application():
    ''' application fixture '''
    database_file_descriptor, database_path = tempfile.mkstemp()

    application = create_app({
        'TESTING': True,
        'DATABASE': database_path,
    })

    with application.app_context():
        init_database()
        get_database().executescript(_data_sql)

    yield application

    os.close(database_file_descriptor)
    os.unlink(database_path)


@pytest.fixture
def client(application):
    ''' client fixture '''
    return application.test_client()


@pytest.fixture
def runner(application):
    ''' runner fixture '''
    return application.test_cli_runner()


class AuthenticationActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='test'):
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/auth/logout')


@pytest.fixture
def authentication(client):
    return AuthenticationActions(client)
