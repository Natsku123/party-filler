import pytest
from fastapi.testclient import TestClient
from test import *


def create_helper(client: TestClient, test_channel, path):
    response = client.post(f"/{path}/", json=test_channel)
    assert response.status_code == 200, response.text
    data = response.json()

    for key, value in test_channel.items():
        assert key in data
        assert data[key] == value

    assert "id" in data
    item_id = data["id"]

    response = client.get(f"/{path}/{item_id}")
    assert response.status_code == 200, response.text

    data = response.json()
    for key, value in test_channel.items():
        assert key in data
        assert data[key] == value

    assert data["id"] == item_id
    return data


@pytest.mark.usefixtures("client")
def test_create_server_1(client: TestClient):
    create_helper(client, TEST_SERVER_1, "servers")


@pytest.mark.usefixtures("client")
def test_create_server_2(client: TestClient):
    create_helper(client, TEST_SERVER_2, "servers")


@pytest.mark.usefixtures("client")
def test_create_server_no_id(client: TestClient):
    response = client.post("/servers/", json=TEST_SERVER_NO_ID)
    assert response.status_code == 422, response.text


@pytest.mark.usefixtures("client")
def test_create_server_no_name(client: TestClient):
    response = client.post("/servers/", json=TEST_SERVER_NO_NAME)
    assert response.status_code == 422, response.text


@pytest.mark.usefixtures("client")
def create_channel_test_helper(client: TestClient, test_channel):
    create_helper(client, test_channel, "channels")


@pytest.mark.usefixtures("client")
def test_create_channel_1(client: TestClient, create_deps=True):
    if create_deps:
        test_create_server_1(client)
        test_create_server_2(client)
    create_helper(client, TEST_CHANNEL_1, "channels")


@pytest.mark.usefixtures("client")
def test_create_channel_2(client: TestClient, create_deps=True):
    if create_deps:
        test_create_server_1(client)
        test_create_server_2(client)
    create_helper(client, TEST_CHANNEL_2, "channels")


@pytest.mark.usefixtures("client")
def test_create_channel_no_name(client: TestClient, create_deps=True):
    if create_deps:
        test_create_server_1(client)
        test_create_server_2(client)
    response = client.post("/channels/", json=TEST_CHANNEL_NO_NAME)
    assert response.status_code == 400, response.text


@pytest.mark.usefixtures("client")
def test_create_channel_no_id(client: TestClient, create_deps=True):
    if create_deps:
        test_create_server_1(client)
        test_create_server_2(client)
    response = client.post("/channels/", json=TEST_CHANNEL_NO_ID)
    assert response.status_code == 422, response.text


@pytest.mark.usefixtures("client")
def test_create_channel_no_server(client: TestClient, create_deps=True):
    if create_deps:
        test_create_server_1(client)
        test_create_server_2(client)
    response = client.post("/channels/", json=TEST_CHANNEL_NO_SERVER)
    assert response.status_code == 400, response.text


@pytest.mark.usefixtures("client")
def test_create_game_1(client: TestClient):
    create_helper(client, TEST_GAME_1, "games")


@pytest.mark.usefixtures("client")
def test_create_game_2(client: TestClient):
    create_helper(client, TEST_GAME_2, "games")


@pytest.mark.usefixtures("client")
def test_create_game_no_name(client: TestClient):
    response = client.post("/games/", json=TEST_GAME_NO_NAME)
    assert response.status_code == 422, response.text


@pytest.mark.usefixtures("client")
def test_create_party_1(client: TestClient, create_deps=True):
    if create_deps:
        test_create_game_1(client)
        test_create_game_2(client)
    party_helper(client, TEST_PARTY_1)


@pytest.mark.usefixtures("client")
def test_create_party_2(client: TestClient, create_deps=True):
    if create_deps:
        test_create_game_1(client)
        test_create_game_2(client)
    party_helper(client, TEST_PARTY_2)


def validate_test_party(test_party, data):
    for key, value in test_party.items():
        assert key in data
        assert data[key] == value

    assert "id" in data
    assert "game" in data
    assert "leader" in data
    assert data["game"] != "null" and data["game"] is not None
    assert data["leader"] != "null" and data["game"] is not None


def party_helper(client: TestClient, test_party):
    response = client.post("/parties/", json=test_party)
    assert response.status_code == 200, response.text
    data = response.json()
    validate_test_party(test_party, data)

    party_id = data["id"]
    response = client.get(f"/parties/{party_id}")
    assert response.status_code == 200, response.text

    data = response.json()
    validate_test_party(test_party, data)

    assert data["id"] == party_id


@pytest.mark.usefixtures("client")
def test_create_party_no_title(client: TestClient, create_deps=True):
    if create_deps:
        test_create_game_1(client)
        test_create_game_2(client)
    response = client.post("/parties/", json=TEST_PARTY_NO_TITLE)
    assert response.status_code == 422, response.text


@pytest.mark.usefixtures("client")
def test_create_party_no_leader(client: TestClient, create_deps=True):
    if create_deps:
        test_create_game_1(client)
        test_create_game_2(client)
    response = client.post("/parties/", json=TEST_PARTY_NO_LEADER)
    assert response.status_code == 422, response.text


@pytest.mark.usefixtures("client")
def test_create_party_no_game(client: TestClient, create_deps=True):
    if create_deps:
        test_create_game_1(client)
        test_create_game_2(client)
    create_helper(client, TEST_PARTY_NO_GAME, "parties")


@pytest.mark.usefixtures("client")
def test_create_role_1(client: TestClient, create_deps=True):
    if create_deps:
        test_create_game_1(client)
        test_create_game_2(client)
        test_create_party_1(client, False)
        test_create_party_2(client, False)
    create_helper(client, TEST_ROLE_1, "roles")


@pytest.mark.usefixtures("client")
def test_create_role_2(client: TestClient, create_deps=True):
    if create_deps:
        test_create_game_1(client)
        test_create_game_2(client)
        test_create_party_1(client, False)
        test_create_party_2(client, False)
    create_helper(client, TEST_ROLE_2, "roles")


@pytest.mark.usefixtures("client")
def test_create_role_3(client: TestClient, create_deps=True):
    if create_deps:
        test_create_game_1(client)
        test_create_game_2(client)
        test_create_party_1(client, False)
        test_create_party_2(client, False)
    create_helper(client, TEST_ROLE_3, "roles")


def validate_member(data):
    assert "id" in data
    assert "party" in data
    assert "player" in data
    assert data["party"] != "null" and data["party"] is not None
    assert data["player"] != "null" and data["player"] is not None


def create_member_helper(client: TestClient, test_member, should_have_role=False):
    post_response_data = create_helper(client, test_member, "members")

    validate_member(post_response_data)

    member_id = post_response_data["id"]
    response = client.get(f"/members/{member_id}")
    assert response.status_code == 200, response.text
    get_response = response.json()
    for key, value in test_member.items():
        assert key in get_response
        assert get_response[key] == value

    validate_member(get_response)

    if should_have_role:
        assert get_response["role"] != "null" and get_response["role"] is not None
    else:
        assert get_response["role"] != "null" and get_response["role"] is None
    assert get_response["id"] == member_id
    get_party_member_response = client.get(f"/parties/{test_member['partyId']}").json()
    assert "members" in get_party_member_response
    assert id_in_list(get_party_member_response["members"], member_id)


@pytest.mark.usefixtures("client")
def test_create_member_1(client: TestClient, create_deps=True):
    if create_deps:
        test_create_game_1(client)
        test_create_game_2(client)
        test_create_party_1(client, False)
        test_create_party_2(client, False)
        test_create_role_1(client, False)
        test_create_role_2(client, False)
        test_create_role_3(client, False)
    create_member_helper(client, TEST_MEMBER_1)


@pytest.mark.usefixtures("client")
def test_create_member_2(client: TestClient, create_deps=True):
    if create_deps:
        test_create_game_1(client)
        test_create_game_2(client)
        test_create_party_1(client, False)
        test_create_party_2(client, False)
        test_create_role_1(client, False)
        test_create_role_2(client, False)
        test_create_role_3(client, False)
    create_member_helper(client, TEST_MEMBER_2)


@pytest.mark.usefixtures("client")
def test_create_member_3(client: TestClient, create_deps=True):
    if create_deps:
        test_create_game_1(client)
        test_create_game_2(client)
        test_create_party_1(client, False)
        test_create_party_2(client, False)
        test_create_role_1(client, False)
        test_create_role_2(client, False)
        test_create_role_3(client, False)
    create_member_helper(client, TEST_MEMBER_3, True)


@pytest.mark.usefixtures("client")
def test_create_member_no_party(client: TestClient, create_deps=True):
    if create_deps:
        test_create_game_1(client)
        test_create_game_2(client)
        test_create_party_1(client, False)
        test_create_party_2(client, False)
        test_create_role_1(client, False)
        test_create_role_2(client, False)
        test_create_role_3(client, False)
    response = client.post("/members/", json=TEST_MEMBER_NO_PARTY)
    assert response.status_code == 422, response.text


@pytest.mark.usefixtures("client")
def test_create_member_no_player(client: TestClient, create_deps=True):
    if create_deps:
        test_create_game_1(client)
        test_create_game_2(client)
        test_create_party_1(client, False)
        test_create_party_2(client, False)
        test_create_role_1(client, False)
        test_create_role_2(client, False)
        test_create_role_3(client, False)
    response = client.post("/members/", json=TEST_MEMBER_NO_PLAYER)
    assert response.status_code == 422, response.text


def delete_helper(client: TestClient, path: str):
    response = client.get(f"/{path}/")
    assert response.status_code == 200, response.text

    data = response.json()

    assert len(data) > 0

    for item in data:
        del_response = client.delete(f"/{path}/{item['id']}")

        assert del_response.status_code == 200, del_response.text
        del_data = del_response.json()

        for key, value in item.items():
            assert key in del_data
            assert del_data[key] == value

    response = client.get(f"/{path}/")
    assert response.status_code == 200, response.text

    data = response.json()

    assert len(data) == 0


@pytest.mark.usefixtures("client")
def test_delete_members(client: TestClient, create_deps=True):
    if create_deps:
        test_create_game_1(client)
        test_create_game_2(client)
        test_create_party_1(client, False)
        test_create_party_2(client, False)
        test_create_role_1(client, False)
        test_create_role_2(client, False)
        test_create_role_3(client, False)
        test_create_member_1(client, False)
        test_create_member_2(client, False)
        test_create_member_3(client, False)
    delete_helper(client, "members")


@pytest.mark.usefixtures("client")
def test_delete_roles(client: TestClient, create_deps=True):
    if create_deps:
        test_create_game_1(client)
        test_create_game_2(client)
        test_create_party_1(client, False)
        test_create_party_2(client, False)
        test_create_role_1(client, False)
        test_create_role_2(client, False)
        test_create_role_3(client, False)
    delete_helper(client, "roles")


@pytest.mark.usefixtures("client")
def test_delete_parties(client: TestClient, create_deps=True):
    if create_deps:
        test_create_game_1(client)
        test_create_game_2(client)
        test_create_party_1(client, False)
        test_create_party_2(client, False)
    delete_helper(client, "parties")


@pytest.mark.usefixtures("client")
def test_delete_games(client: TestClient, create_deps=True):
    if create_deps:
        test_create_game_1(client)
        test_create_game_2(client)
    delete_helper(client, "games")


@pytest.mark.usefixtures("client")
def test_delete_channels(client: TestClient, create_deps=True):
    test_create_server_1(client)
    test_create_server_2(client)
    if create_deps:
        test_create_channel_1(client, False)
        test_create_channel_2(client, False)
    delete_helper(client, "channels")


@pytest.mark.usefixtures("client")
def test_delete_servers(client: TestClient, create_deps=True):
    if create_deps:
        test_create_server_1(client)
        test_create_server_2(client)
    delete_helper(client, "servers")
