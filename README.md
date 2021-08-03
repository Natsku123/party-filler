# Party Filler
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Find more players to your parties from your Discord-server with Discord integrations 
and party status tracking.

## Webhook format

### on_party_create
```json
{
    "party": {
        "id": 7,
        "title": "Title",
        "leaderId": 1,
        "game": "Game",
        "maxPlayers": 5,
        "minPlayers": 5,
        "description": "Description",
        "channelId": 1,
        "startTime": "1996-10-15T00:05:32Z",
        "endTime": "1996-10-15T00:05:32Z",
        "channel": {
            "id": 1,
            "name": "chat",
            "discordId": "123456789012345678",
            "serverId": 3
        },
        "leader":  {
            "id": 1,
            "discordId": "123456789012345678",
            "name": "Player name",
            "discriminator": "1234",
            "icon": "<icon id>"
        },
        "members": [

        ]
    },
    "event": {
        "name": "on_party_create",
        "datetime": "1996-10-15T00:05:32Z"
    }
}
```
### on_member_join
```json
{
    "member": {
        "id": 4,
        "playerReq": null,
        "partyId": 9,
        "playerId": 1,
        "roleId": null,
        "party": {
            "id": 9,
            "title": "Title",
            "leaderId": 2,
            "game": "Game",
            "maxPlayers": 1,
            "minPlayers": 1,
            "description": "nopee testi - SUORITETTU",
            "channelId": 1,
            "startTime": "1996-10-15T00:05:32Z",
            "endTime": "1996-10-15T00:05:32Z"
        },
        "player": {
            "id": 1,
            "discordId": "123456789012345678",
            "name": "Player name",
            "discriminator": "1234",
            "icon": "<icon id>"
        },
        "role": null
    },
    "channel": {
        "id": 1,
        "name": "chat",
        "discordId": "123456789012345678",
        "serverId": 3
    },
    "event": {
        "name": "on_member_join",
        "datetime": "1996-10-15T00:05:32Z"
    }
}
```
