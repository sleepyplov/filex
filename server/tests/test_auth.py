from filex import db
from filex.models import User


def test_ping(client):
    res = client.get('/api/ping')
    assert b'pong' in res.data


def test_login(client):
    name = 'sleepyplov'
    password = 'qwerty1234'
    user = User(name, password)
    db.session.add(user)
    db.session.commit()
    login_res = client.post('/api/auth/login', json={
        'username': name,
        'password': password,
    }).get_json()
    assert 'access_token' in login_res
    assert 'refresh_token' in login_res
    access_token = login_res['access_token']
    refresh_token = login_res['refresh_token']
    me_res = client.get('/api/auth/me', headers={'Authorization': access_token}).get_json()
    assert 'user' in me_res
    assert me_res['user']['id'] == str(user.id)
    assert me_res['user']['name'] == user.name
