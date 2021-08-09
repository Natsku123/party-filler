from test.test_main import client
from test import *


def create_helper(test_channel, path):
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


def test_create_server_1():
    create_helper(TEST_SERVER_1, "servers")


def test_create_server_2():
    create_helper(TEST_SERVER_2, "servers")


def test_create_server_no_id():
    response = client.post("/servers/", json=TEST_SERVER_NO_ID)
    assert response.status_code == 422, response.text


def test_create_server_no_name():
    response = client.post("/servers/", json=TEST_SERVER_NO_NAME)
    assert response.status_code == 422, response.text


def create_channel_test_helper(test_channel):
    create_helper(test_channel, "channels")


def test_create_channel_1():
    create_helper(TEST_CHANNEL_1, "channels")


def test_create_channel_2():
    create_helper(TEST_CHANNEL_2, "channels")


def test_create_channel_no_name():
    response = client.post("/channels/", json=TEST_CHANNEL_NO_NAME)
    assert response.status_code == 400, response.text


def test_create_channel_no_id():
    response = client.post("/channels/", json=TEST_CHANNEL_NO_ID)
    assert response.status_code == 422, response.text


def test_create_channel_no_server():
    response = client.post("/channels/", json=TEST_CHANNEL_NO_SERVER)
    assert response.status_code == 400, response.text


def test_create_game_1():
    create_helper(TEST_GAME_1, "games")


def test_create_game_2():
    create_helper(TEST_GAME_2, "games")


def test_create_game_no_name():
    response = client.post("/games/", json=TEST_GAME_NO_NAME)
    assert response.status_code == 422, response.text


def test_create_party_1():
    party_helper(TEST_PARTY_1)


def test_create_party_2():
    party_helper(TEST_PARTY_2)


def validate_test_party(test_party, data):
    for key, value in test_party.items():
        assert key in data
        assert data[key] == value

    assert "id" in data
    assert "game" in data
    assert "leader" in data
    assert data["game"] != "null" and data["game"] is not None
    assert data["leader"] != "null" and data["game"] is not None


def party_helper(test_party):
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


def test_create_party_no_title():
    response = client.post("/parties/", json=TEST_PARTY_NO_TITLE)
    assert response.status_code == 422, response.text


def test_create_party_no_leader():
    response = client.post("/parties/", json=TEST_PARTY_NO_LEADER)
    assert response.status_code == 422, response.text


def test_create_party_no_game():
    response = client.post("/parties/", json=TEST_PARTY_NO_GAME)
    assert response.status_code == 422, response.text


def test_create_role_1():
    create_helper(TEST_ROLE_1, "roles")


def test_create_role_2():
    create_helper(TEST_ROLE_2, "roles")


def test_create_role_3():
    create_helper(TEST_ROLE_3, "roles")


def validate_member(data):
    assert "id" in data
    assert "party" in data
    assert "player" in data
    assert data["party"] != "null" and data["party"] is not None
    assert data["player"] != "null" and data["player"] is not None


def create_member_helper(test_member, should_have_role=False):
    post_response_data = create_helper(test_member, "members")

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


def test_create_member_1():
    create_member_helper(TEST_MEMBER_1)


def test_create_member_2():
    create_member_helper(TEST_MEMBER_2)


def test_create_member_3():
    create_member_helper(TEST_MEMBER_3, True)


def test_create_member_no_party():
    response = client.post("/members/", json=TEST_MEMBER_NO_PARTY)
    assert response.status_code == 422, response.text


def test_create_member_no_player():
    response = client.post("/members/", json=TEST_MEMBER_NO_PLAYER)
    assert response.status_code == 422, response.text


def delete_helper(path: str):
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


def test_delete_members():
    delete_helper("members")


def test_delete_roles():
    delete_helper("roles")


def test_delete_parties():
    delete_helper("parties")


def test_delete_games():
    delete_helper("games")


def test_delete_channels():
    delete_helper("channels")


def test_delete_servers():
    delete_helper("servers")
