from flaskr import create_app


def test_config():
    ''' test configuration '''
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing

def test_hello(client):
    ''' test the /hello route path '''
    response = client.get('/hello')
    assert response.data == b'Hello, World!'
