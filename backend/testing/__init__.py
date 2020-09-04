import datetime

TEST_PLAYER_1 = {
    "discordId": "1234567890",
    "name": "TEST PLAYER 1",
    "discriminator": "0001"
}

TEST_PLAYER_2 = {
    "discordId": "0987654321",
    "name": "TEST PLAYER 2",
    "discriminator": "0002",
    "icon": "asd"
}

TEST_PLAYER_NO_ID = {
    "name": "TEST PLAYER 3",
    "discriminator": "0003"
}

TEST_PLAYER_NO_NAME = {
    "discordId": "1111111111",
    "discriminator": "0004"
}

TEST_PLAYER_NO_DISC = {
    "discord_id": "2222222222",
    "name": "TEST PLAYER 5",
    "discriminator": "0005"
}

TEST_SERVER_1 = {
    "name": "TEST SERVER 1",
    "discordId": "1234567890"
}

TEST_SERVER_2 = {
    "name": "TEST SERVER 2",
    "discordId": "0987654321",
    "icon": "asd"
}

TEST_SERVER_NO_ID = {
    "name": "TEST SERVER 1"
}

TEST_SERVER_NO_NAME = {
    "discordId": "1234567890"
}

TEST_CHANNEL_1 = {
    "name": "test-chat",
    "discordId": "1234567890",
    "serverId": 1
}

TEST_CHANNEL_2 = {
    "name": "asd-chat",
    "discordId": "0987654321",
    "serverId": 2
}

TEST_CHANNEL_NO_ID = {
    "name": "asdasd-chat",
    "serverId": 1
}

TEST_CHANNEL_NO_NAME = {
    "discordId": "1111111111",
    "serverId": 1
}

TEST_CHANNEL_NO_SERVER = {
    "name": "kappa-chat",
    "discordId": "2222222222",
}

TEST_MEMBER_1 = {
    "partyId": 1,
    "playerId": 1,
}

TEST_MEMBER_2 = {
    "partyId": 1,
    "playerId": 1,
    "playerReq": 10
}

TEST_MEMBER_3 = {
    "partyId": 1,
    "playerId": 1,
    "roleId": 10
}

TEST_MEMBER_NO_PARTY = {
    "playerId": 1,
    "playerReq": 10
}

TEST_MEMBER_NO_PLAYER = {
    "partyId": 1,
    "playerReq": 10
}

TEST_PARTY_1 = {
    "title": "nice party",
    "leaderId": 1,
    "gameId": 1,
}

TEST_PARTY_2 = {
    "title": "nice party",
    "leaderId": 1,
    "gameId": 1,
    "maxPlayers": 10,
    "minPlayers": 1,
    "description": "asdasd",
    "channelId": 1,
    "startTime": datetime.datetime.now(),
    "endTime": datetime.datetime.now()
}

TEST_PARTY_NO_TITLE = {
    "leaderId": 1,
    "gameId": 1,
}

TEST_PARTY_NO_LEADER = {
    "title": "nice party",
    "gameId": 1,
}

TEST_PARTY_NO_GAME = {
    "title": "nice party",
    "leaderId": 1,
}

TEST_ROLE_1 = {
    "name": "nice"
}

TEST_ROLE_2 = {
    "name": "nicer",
    "partyId": 1
}

TEST_ROLE_3 = {
    "name": "nicest",
    "maxPlayers": 1
}

TEST_GAME_1 = {
    "name": "good game"
}

TEST_GAME_2 = {
    "name": "best game",
    "defaultMaxPlayers": 10
}

TEST_GAME_NO_NAME = {
    "defaultMaxPlayers": 10
}

TEST_EMPTY = {

}


def id_in_list(list, id):
    for item in list:
        if item["id"] == id:
            return True
    return False
