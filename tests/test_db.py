import sqlite3

import pytest
from flaskr.db import get_database


def test_get_close_db(application):
    ''' test the get and close database '''
    with application.app_context():
        database = get_database()
        assert database is get_database()

    with pytest.raises(sqlite3.ProgrammingError) as error:
        database.execute('SELECT 1')

    assert 'closed' in str(error.value)

def test_init_db_command(runner, monkeypatch):
    class Recorder(object):
        called = False

    def fake_init_db():
        Recorder.called = True

    monkeypatch.setattr('flaskr.db.init_database', fake_init_db)
    result = runner.invoke(args=['init-db'])
    assert 'Database Initialized' in result.output
    assert Recorder.called
