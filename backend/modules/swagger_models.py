# flask-restful-swagger doesn't support SQLAlchemy models
# so here is some dummy models
import datetime
from flask_restful_swagger import swagger


@swagger.model
class OAuth2Token:
    def __init__(
            self,
            player_id: int,
            name: str,
            token_type: str,
            access_token: str,
            refresh_token: str,
            expires_at: int
    ):
        pass


@swagger.model
class Server:
    def __init__(
            self,
            name: str,
            icon: str,
            discord_id: str,
            channels: list,
            players: list,
    ):
        pass


@swagger.model
class Channel:
    def __init__(
            self,
            name: str,
            discord_id: str,
            server_id: int
    ):
        pass


@swagger.model
class Player:
    def __init__(
            self,
            discord_id: str,
            name: str,
            icon: str,
            servers: list,
    ):
        pass


@swagger.model
class Party:
    def __init__(
            self,
            title: str,
            leader_id: int,
            game: str,
            max_players: int,
            min_players: int,
            description: str,
            channel_id: int,
            start_time: datetime.datetime,
            end_time: datetime.datetime,
            channel: Channel,
            leader: Player,
            members: list
    ):
        pass


@swagger.model
class Role:
    def __init__(
            self,
            party_id: int,
            name: str,
            max_players: int,
            party: Party
    ):
        pass


@swagger.model
class Member:
    def __init__(
            self,
            player_req: int,
            party_id: int,
            player_id: int,
            role_id: int,

            party: Party,
            player: Player,
            role: Role
    ):
        pass
