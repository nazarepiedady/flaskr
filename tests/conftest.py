import os
import tempfile

import pytest
from flaskr import create_app
from flaskr.db import get_database, init_database


with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as file:
    __data_sql = file.read().decode('utf-8')


@pytest.fixture
def application():
    database_file_directory, database_path = tempfile.mkstemp()

    application = create_app({
        'TESTING': True,
        'DATABASE': database_path,
    })

    with application.app_context():
        init_database()
        get_database().executescript(__data_sql)

    yield application

    os.close(database_file_directory)
    os.unlink(database_path)


@pytest.fixture
def client(application):
    return application.test_client()
