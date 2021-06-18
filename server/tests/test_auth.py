def test_ping(client):
    res = client.get('/ping')
    assert b'pong' in res.data
