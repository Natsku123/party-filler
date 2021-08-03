# Party Filler
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Docker](https://github.com/Natsku123/party-filler/actions/workflows/docker-publish.yml/badge.svg)](https://github.com/Natsku123/party-filler/actions/workflows/docker-publish.yml)

Find more players to your parties from your Discord-server with Discord integrations 
and party status tracking.

## Installation

### Discord

TODO: Add guide.

### Manual

TODO: Add proper guide.

You could install it manually though it is not recommended, since the stack was built and designed to be run inside Docker.

### Docker Compose (Recommended)

All necessary files needed to run PartyFiller can be found in `example` folder. The example `docker-compose.yml` file includes a Traefik service which you can use or setup separately and connect to the `traefiknet` network. You could also use some other reverse proxy in front of the services.

Create a network for Traefik.
```bash
docker network create traefiknet
```

Copy traefik.yml into the traefik folder for example `/srv/docker/traefik`, make sure that the path is the same in the `docker-compose.yml` file.

Move / copy `docker-compose.yml` and `example.env` to some new directory for example `/srv/docker/partyfiller`.

Rename `example.env` into `.env` and make changes described in `docker-compose.yml` and change all values `CHANGE_ME` and `FROM_DISCORD` to appropriate values. `FROM_DISCORD` values are described and given in the [Discord](#discord) section.

After the modifications you can just start the stack:
```bash
docker-compose up -d
```

### Docker without Compose (Recommended)

TODO: Add guide.

## General

### Data Formats

#### Webhooks

<details>
<summary>on_party_create</summary>
<p>

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
            "icon": "iconHash"
        },
        "members": []
    },
    "event": {
        "name": "on_party_create",
        "datetime": "1996-10-15T00:05:32Z"
    }
}
```
</p>
</details>
<details>
<summary>on_member_join</summary>
<p>
        
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
            "icon": "iconHash"
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
</p>
</details>
