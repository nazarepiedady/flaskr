from flaskr import create_app


def test_config():
    ''' test configuration '''
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing
