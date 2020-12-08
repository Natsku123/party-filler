from test.test_main import client
from test import *


def test_create_server_1():
    response = client.post(
        '/servers/',
        json=TEST_SERVER_1
    )
    assert response.status_code == 200, response.text
    data = response.json()

    for key, value in TEST_SERVER_1.items():
        assert key in data
        assert data[key] == value

    assert "id" in data
    server_id = data["id"]

    response = client.get(f'/servers/{server_id}')
    assert response.status_code == 200, response.text

    data = response.json()
    for key, value in TEST_SERVER_1.items():
        assert key in data
        assert data[key] == value

    assert data["id"] == server_id


def test_create_server_2():
    response = client.post(
        '/servers/',
        json=TEST_SERVER_2
    )
    assert response.status_code == 200, response.text
    data = response.json()

    for key, value in TEST_SERVER_2.items():
        assert key in data
        assert data[key] == value

    assert "id" in data
    server_id = data["id"]

    response = client.get(f'/servers/{server_id}')
    assert response.status_code == 200, response.text

    data = response.json()
    for key, value in TEST_SERVER_2.items():
        assert key in data
        assert data[key] == value

    assert data["id"] == server_id


def test_create_server_no_id():
    response = client.post(
        '/servers/',
        json=TEST_SERVER_NO_ID
    )
    assert response.status_code == 422, response.text


def test_create_server_no_name():
    response = client.post(
        '/servers/',
        json=TEST_SERVER_NO_NAME
    )
    assert response.status_code == 422, response.text


def test_create_channel_1():
    response = client.post(
        '/channels/',
        json=TEST_CHANNEL_1
    )
    assert response.status_code == 200, response.text
    data = response.json()

    for key, value in TEST_CHANNEL_1.items():
        assert key in data
        assert data[key] == value

    assert "id" in data
    channel_id = data["id"]

    response = client.get(f'/channels/{channel_id}')
    assert response.status_code == 200, response.text

    data = response.json()
    for key, value in TEST_CHANNEL_1.items():
        assert key in data
        assert data[key] == value

    assert data["id"] == channel_id


def test_create_channel_2():
    response = client.post(
        '/channels/',
        json=TEST_CHANNEL_2
    )
    assert response.status_code == 200, response.text
    data = response.json()

    for key, value in TEST_CHANNEL_2.items():
        assert key in data
        assert data[key] == value

    assert "id" in data
    channel_id = data["id"]

    response = client.get(f'/channels/{channel_id}')
    assert response.status_code == 200, response.text

    data = response.json()
    for key, value in TEST_CHANNEL_2.items():
        assert key in data
        assert data[key] == value

    assert data["id"] == channel_id


def test_create_channel_no_name():
    response = client.post(
        '/channels/',
        json=TEST_CHANNEL_NO_NAME
    )
    assert response.status_code == 400, response.text


def test_create_channel_no_id():
    response = client.post(
        '/channels/',
        json=TEST_CHANNEL_NO_ID
    )
    assert response.status_code == 422, response.text


def test_create_channel_no_server():
    response = client.post(
        '/channels/',
        json=TEST_CHANNEL_NO_SERVER
    )
    assert response.status_code == 400, response.text


def test_create_game_1():
    response = client.post(
        '/games/',
        json=TEST_GAME_1
    )
    assert response.status_code == 200, response.text
    data = response.json()

    for key, value in TEST_GAME_1.items():
        assert key in data
        assert data[key] == value

    assert "id" in data
    game_id = data["id"]

    response = client.get(f'/games/{game_id}')
    assert response.status_code == 200, response.text

    data = response.json()
    for key, value in TEST_GAME_1.items():
        assert key in data
        assert data[key] == value

    assert data["id"] == game_id


def test_create_game_2():
    response = client.post(
        '/games/',
        json=TEST_GAME_2
    )
    assert response.status_code == 200, response.text
    data = response.json()

    for key, value in TEST_GAME_2.items():
        assert key in data
        assert data[key] == value

    assert "id" in data
    game_id = data["id"]

    response = client.get(f'/games/{game_id}')
    assert response.status_code == 200, response.text

    data = response.json()
    for key, value in TEST_GAME_2.items():
        assert key in data
        assert data[key] == value

    assert data["id"] == game_id


def test_create_game_no_name():
    response = client.post(
        '/games/',
        json=TEST_GAME_NO_NAME
    )
    assert response.status_code == 422, response.text


def test_create_party_1():
    response = client.post(
        '/parties/',
        json=TEST_PARTY_1
    )
    assert response.status_code == 200, response.text
    data = response.json()

    for key, value in TEST_PARTY_1.items():
        assert key in data
        assert data[key] == value

    assert "id" in data
    assert "game" in data
    assert "leader" in data
    assert data["game"] != "null" and data["game"] is not None
    assert data["leader"] != "null" and data["game"] is not None

    party_id = data["id"]

    response = client.get(f'/parties/{party_id}')
    assert response.status_code == 200, response.text

    data = response.json()
    for key, value in TEST_PARTY_1.items():
        assert key in data
        assert data[key] == value

    assert "id" in data
    assert "game" in data
    assert "leader" in data
    assert data["game"] != "null" and data["game"] is not None
    assert data["leader"] != "null" and data["game"] is not None

    assert data["id"] == party_id


def test_create_party_2():
    response = client.post(
        '/parties/',
        json=TEST_PARTY_2
    )
    assert response.status_code == 200, response.text
    data = response.json()

    for key, value in TEST_PARTY_2.items():
        assert key in data
        assert data[key] == value

    assert "id" in data
    assert "game" in data
    assert "leader" in data
    assert data["game"] != "null" and data["game"] is not None
    assert data["leader"] != "null" and data["game"] is not None

    party_id = data["id"]

    response = client.get(f'/parties/{party_id}')
    assert response.status_code == 200, response.text

    data = response.json()
    for key, value in TEST_PARTY_2.items():
        assert key in data
        assert data[key] == value

    assert "id" in data
    assert "game" in data
    assert "leader" in data
    assert data["game"] != "null" and data["game"] is not None
    assert data["leader"] != "null" and data["game"] is not None

    assert data["id"] == party_id


def test_create_party_no_title():
    response = client.post(
        '/parties/',
        json=TEST_PARTY_NO_TITLE
    )
    assert response.status_code == 422, response.text


def test_create_party_no_leader():
    response = client.post(
        '/parties/',
        json=TEST_PARTY_NO_LEADER
    )
    assert response.status_code == 422, response.text


def test_create_party_no_game():
    response = client.post(
        '/parties/',
        json=TEST_PARTY_NO_GAME
    )
    assert response.status_code == 422, response.text


def test_create_role_1():
    response = client.post(
        '/roles/',
        json=TEST_ROLE_1
    )
    assert response.status_code == 200, response.text
    data = response.json()

    for key, value in TEST_ROLE_1.items():
        assert key in data
        assert data[key] == value

    assert "id" in data
    role_id = data["id"]

    response = client.get(f'/roles/{role_id}')
    assert response.status_code == 200, response.text

    data = response.json()
    for key, value in TEST_ROLE_1.items():
        assert key in data
        assert data[key] == value

    assert data["id"] == role_id


def test_create_role_2():
    response = client.post(
        '/roles/',
        json=TEST_ROLE_2
    )
    assert response.status_code == 200, response.text
    data = response.json()

    for key, value in TEST_ROLE_2.items():
        assert key in data
        assert data[key] == value

    assert "id" in data
    role_id = data["id"]

    response = client.get(f'/roles/{role_id}')
    assert response.status_code == 200, response.text

    data = response.json()
    for key, value in TEST_ROLE_2.items():
        assert key in data
        assert data[key] == value

    assert data["id"] == role_id


def test_create_role_3():
    response = client.post(
        '/roles/',
        json=TEST_ROLE_3
    )
    assert response.status_code == 200, response.text
    data = response.json()

    for key, value in TEST_ROLE_3.items():
        assert key in data
        assert data[key] == value

    assert "id" in data
    role_id = data["id"]

    response = client.get(f'/roles/{role_id}')
    assert response.status_code == 200, response.text

    data = response.json()
    for key, value in TEST_ROLE_3.items():
        assert key in data
        assert data[key] == value

    assert data["id"] == role_id


def test_create_member_1():
    response = client.post(
        '/members/',
        json=TEST_MEMBER_1
    )
    assert response.status_code == 200, response.text
    data = response.json()

    for key, value in TEST_MEMBER_1.items():
        assert key in data
        assert data[key] == value

    assert "id" in data
    assert "party" in data
    assert "player" in data
    assert data["party"] != "null" and data["party"] is not None
    assert data["player"] != "null" and data["player"] is not None

    member_id = data["id"]

    response = client.get(f'/members/{member_id}')
    assert response.status_code == 200, response.text

    data = response.json()
    for key, value in TEST_MEMBER_1.items():
        assert key in data
        assert data[key] == value

    assert "party" in data
    assert "player" in data
    assert "role" in data
    assert "id" in data
    assert data["party"] != "null" and data["party"] is not None
    assert data["player"] != "null" and data["player"] is not None
    assert data["role"] != "null" and data["role"] is not None

    assert data["id"] == member_id

    response = client.get(f"/parties/{TEST_MEMBER_1['party_id']}")
    data = response.json()

    assert "members" in data
    assert id_in_list(data["members"], member_id)


def test_create_member_2():
    response = client.post(
        '/members/',
        json=TEST_MEMBER_2
    )
    assert response.status_code == 200, response.text
    data = response.json()

    for key, value in TEST_MEMBER_2.items():
        assert key in data
        assert data[key] == value

    assert "id" in data
    assert "party" in data
    assert "player" in data
    assert data["party"] != "null" and data["party"] is not None
    assert data["player"] != "null" and data["player"] is not None

    member_id = data["id"]

    response = client.get(f'/members/{member_id}')
    assert response.status_code == 200, response.text

    data = response.json()
    for key, value in TEST_MEMBER_2.items():
        assert key in data
        assert data[key] == value

    assert "party" in data
    assert "player" in data
    assert "role" in data
    assert "id" in data
    assert data["party"] != "null" and data["party"] is not None
    assert data["player"] != "null" and data["player"] is not None
    assert data["role"] != "null" and data["role"] is not None

    assert data["id"] == member_id

    response = client.get(f"/parties/{TEST_MEMBER_2['party_id']}")
    data = response.json()

    assert "members" in data
    assert id_in_list(data["members"], member_id)


def test_create_member_3():
    response = client.post(
        '/members/',
        json=TEST_MEMBER_3
    )
    assert response.status_code == 200, response.text
    data = response.json()

    for key, value in TEST_MEMBER_3.items():
        assert key in data
        assert data[key] == value

    assert "id" in data
    assert "party" in data
    assert "player" in data
    assert "role" in data
    assert data["party"] != "null" and data["party"] is not None
    assert data["player"] != "null" and data["player"] is not None
    assert data["role"] != "null" and data["role"] is not None

    member_id = data["id"]

    response = client.get(f'/members/{member_id}')
    assert response.status_code == 200, response.text

    data = response.json()
    for key, value in TEST_MEMBER_3.items():
        assert key in data
        assert data[key] == value

    assert "party" in data
    assert "player" in data
    assert "role" in data
    assert "id" in data
    assert data["party"] != "null" and data["party"] is not None
    assert data["player"] != "null" and data["player"] is not None
    assert data["role"] != "null" and data["role"] is not None

    assert data["id"] == member_id

    response = client.get(f"/parties/{TEST_MEMBER_3['party_id']}")
    data = response.json()

    assert "members" in data
    assert id_in_list(data["members"], member_id)


def test_create_member_no_party():
    response = client.post(
        '/members/',
        json=TEST_MEMBER_NO_PARTY
    )
    assert response.status_code == 422, response.text


def test_create_member_no_player():
    response = client.post(
        '/members/',
        json=TEST_MEMBER_NO_PLAYER
    )
    assert response.status_code == 422, response.text


def test_delete_members():
    response = client.get('/members/')
    assert response.status_code == 200, response.text

    data = response.json()

    assert len(data) > 0

    for member in data:
        del_response = client.delete(f"/members/{member['id']}")

        assert del_response.status_code == 200, response.text
        del_data = del_response.json()

        for key, value in member.items():
            assert key in del_data
            assert del_data[key] == value

    response = client.get('/members/')
    assert response.status_code == 200, response.text

    data = response.json()

    assert len(data) == 0


def test_delete_roles():
    response = client.get('/roles/')
    assert response.status_code == 200, response.text

    data = response.json()

    assert len(data) > 0

    for role in data:
        del_response = client.delete(f"/roles/{role['id']}")

        assert del_response.status_code == 200, response.text
        del_data = del_response.json()

        for key, value in role.items():
            assert key in del_data
            assert del_data[key] == value

    response = client.get('/roles/')
    assert response.status_code == 200, response.text

    data = response.json()

    assert len(data) == 0


def test_delete_parties():
    response = client.get('/parties/')
    assert response.status_code == 200, response.text

    data = response.json()

    assert len(data) > 0

    for party in data:
        del_response = client.delete(f"/parties/{party['id']}")

        assert del_response.status_code == 200, response.text
        del_data = del_response.json()

        for key, value in party.items():
            assert key in del_data
            assert del_data[key] == value

    response = client.get('/parties/')
    assert response.status_code == 200, response.text

    data = response.json()

    assert len(data) == 0


def test_delete_games():
    response = client.get('/games/')
    assert response.status_code == 200, response.text

    data = response.json()

    assert len(data) > 0

    for game in data:
        del_response = client.delete(f"/games/{game['id']}")

        assert del_response.status_code == 200, response.text
        del_data = del_response.json()

        for key, value in game.items():
            assert key in del_data
            assert del_data[key] == value

    response = client.get('/games/')
    assert response.status_code == 200, response.text

    data = response.json()

    assert len(data) == 0


def test_delete_channels():
    response = client.get('/channels/')
    assert response.status_code == 200, response.text

    data = response.json()

    assert len(data) > 0

    for channel in data:
        del_response = client.delete(f"/channels/{channel['id']}")

        assert del_response.status_code == 200, response.text

    response = client.get('/channels/')
    assert response.status_code == 200, response.text

    data = response.json()

    assert len(data) == 0


def test_delete_servers():
    response = client.get('/servers/')
    assert response.status_code == 200, response.text

    data = response.json()

    assert len(data) > 0

    for server in data:
        del_response = client.delete(f"/servers/{server['id']}")

        assert del_response.status_code == 200, response.text

    response = client.get('/servers/')
    assert response.status_code == 200, response.text

    data = response.json()

    assert len(data) == 0
