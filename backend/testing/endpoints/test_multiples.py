from testing.test_main import client


def test_get_current_player():
    response = client.get('/players/')
    assert response.status_code == 200, response.text


def test_get_servers():
    response = client.get('/servers/')
    assert response.status_code == 200, response.text


def test_get_parties():
    response = client.get('/parties/')
    assert response.status_code == 200, response.text


def test_get_members():
    response = client.get('/members/')
    assert response.status_code == 200, response.text


def test_get_channels():
    response = client.get('/channels/')
    assert response.status_code == 200, response.text


def test_get_games():
    response = client.get('/games/')
    assert response.status_code == 200, response.text


def test_get_roles():
    response = client.get('/roles/')
    assert response.status_code == 200, response.text
