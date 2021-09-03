import pytest
from fastapi.testclient import TestClient


@pytest.mark.usefixtures("client")
def test_get_current_player(client: TestClient):
    response = client.get("/players/")
    assert response.status_code == 200, response.text


@pytest.mark.usefixtures("client")
def test_get_servers(client: TestClient):
    response = client.get("/servers/")
    assert response.status_code == 200, response.text


@pytest.mark.usefixtures("client")
def test_get_parties(client: TestClient):
    response = client.get("/parties/")
    assert response.status_code == 200, response.text


@pytest.mark.usefixtures("client")
def test_get_members(client: TestClient):
    response = client.get("/members/")
    assert response.status_code == 200, response.text


@pytest.mark.usefixtures("client")
def test_get_channels(client: TestClient):
    response = client.get("/channels/")
    assert response.status_code == 200, response.text


@pytest.mark.usefixtures("client")
def test_get_games(client: TestClient):
    response = client.get("/games/")
    assert response.status_code == 200, response.text


@pytest.mark.usefixtures("client")
def test_get_roles(client: TestClient):
    response = client.get("/roles/")
    assert response.status_code == 200, response.text
