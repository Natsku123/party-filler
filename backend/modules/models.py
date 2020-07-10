import datetime
import modules.utils
from modules.utils import base_serialize, datetime_to_string
from flask_sqlalchemy import SQLAlchemy
from flask_restful_swagger import swagger

db = SQLAlchemy()

player_server_association = db.Table(
    'players_servers',
    db.Column('player_id', db.Integer, db.ForeignKey('players.id')),
    db.Column('server_id', db.Integer, db.ForeignKey('servers.id'))
)


# Forward declarations
class Player:
    pass


class Party:
    pass


class Role:
    pass


@modules.utils.model
class OAuth2Token(db.Model):
    token_id = db.Column(db.Integer, primary_key=True, nullable=False)
    player_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    name = db.Column(db.String(20), nullable=False)

    player = db.relationship('Player')

    token_type = db.Column(db.String(20))
    access_token = db.Column(db.String(48), nullable=False)
    refresh_token = db.Column(db.String(48))
    expires_at = db.Column(db.Integer, default=0)

    swagger_metadata = {
        "token_id": {
            "type": int.__name__
        },
        "player_id": {
            "type": int.__name__
        },
        "name": {
            "type": str.__name__
        },
        "player": {
            "type": Player.__name__
        },
        "token_type": {
            "type": str.__name__
        },
        "access_token": {
            "type": str.__name__
        },
        "refresh_token": {
            "type": str.__name__
        },
        "expires_at": {
            "type": int.__name__,
            "default": 0
        }
    }

    def to_token(self):
        return dict(
            access_token=self.access_token,
            token_type=self.token_type,
            refresh_token=self.refresh_token,
            expires_at=self.expires_at,
        )


@modules.utils.model
class Server(db.Model):
    __tablename__ = 'servers'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(255), nullable=False)
    icon = db.Column(db.String(64))
    discord_id = db.Column(db.String(64), nullable=False, unique=True)

    channels = db.relationship('Channel', backref=db.backref('server', lazy=True))
    players = db.relationship('Player', secondary=player_server_association, back_populates="servers")

    swagger_metadata = {
        "id": {
            "type": int.__name__
        },
        "name": {
            "type": str.__name__
        },
        "icon": {
            "type": str.__name__
        },
        "discord_id": {
            "type": str.__name__
        },
        "channels": {
            "type": list.__name__
        },
        "players": {
            "type": list.__name__
        }
    }

    def base_serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "icon": self.icon,
            "discord_id": self.discord_id
        }

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "icon": self.icon,
            "discord_id": self.discord_id,
            "channels": list(map(lambda channel: channel.base_serialize(), self.channels))
        }


@modules.utils.model
class Channel(db.Model):
    __tablename__ = 'channels'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(255), nullable=False)
    discord_id = db.Column(db.String(64), nullable=False, unique=True)
    server_id = db.Column(db.Integer, db.ForeignKey('servers.id'), nullable=False)

    swagger_metadata = {
        "id": {
            "type": int.__name__
        },
        "name": {
            "type": str.__name__
        },
        "discord_id": {
            "type": str.__name__
        },
        "server_id": {
            "type": int.__name__
        }
    }

    def base_serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "discord_id": self.discord_id,
            "server_id": self.server_id,
        }

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "discord_id": self.discord_id,
            "server_id": self.server_id,
            "server": base_serialize(self.server)
        }


@modules.utils.model
class Player(db.Model):
    __tablename__ = 'players'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    discord_id = db.Column(db.String(64), nullable=False, unique=True)
    name = db.Column(db.String(64), nullable=False)
    discriminator = db.Column(db.String(4), nullable=False)
    icon = db.Column(db.String(64))

    # Flask-Login
    is_authenticated = db.Column(db.Boolean, nullable=False, default=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    is_anonymous = db.Column(db.Boolean, nullable=False, default=False)

    servers = db.relationship('Server', secondary=player_server_association, back_populates="players")

    swagger_metadata = {
        "id": {
            "type": int.__name__
        },
        "name": {
            "type": str.__name__
        },
        "discriminator": {
            "type": str.__name__
        },
        "icon": {
            "type": str.__name__
        },
        "discord_id": {
            "type": str.__name__
        },
        "servers": {
            "type": list.__name__
        }
    }

    def get_id(self):
        return str(self.id)

    def base_serialize(self):
        return {
            "id": self.id,
            "discord_id": self.discord_id,
            "name": self.name,
            "discriminator": self.discriminator,
            "icon": self.icon
        }

    def serialize(self):
        return {
            "id": self.id,
            "discord_id": self.discord_id,
            "name": self.name,
            "discriminator": self.discriminator,
            "icon": self.icon,
            "servers": list(map(lambda server: server.base_serialize(), self.servers))
        }


@modules.utils.model
class Member(db.Model):
    __tablename__ = 'members'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    player_req = db.Column(db.Integer)
    party_id = db.Column(db.Integer, db.ForeignKey('parties.id'), nullable=False)
    player_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    party = db.relationship('Party')
    player = db.relationship('Player')
    role = db.relationship('Role')

    swagger_metadata = {
        "id": {
            "type": int.__name__
        },
        "player_req": {
            "type": int.__name__
        },
        "party_id": {
            "type": int.__name__
        },
        "player_id": {
            "type": int.__name__
        },
        "role_id": {
            "type": int.__name__
        },
        "party": {
            "type": Party.__name__
        },
        "player": {
            "type": Player.__name__
        },
        "role": {
            "type": Role.__name__
        }
    }

    def base_serialize(self):
        return {
            "id": self.id,
            "player_req": self.player_req,
            "party_id": self.party_id,
            "player_id": self.player_id,
            "role_id": self.role_id
        }

    def serialize(self):
        return {
            "id": self.id,
            "player_req": self.player_req,
            "party_id": self.party_id,
            "player_id": self.player_id,
            "role_id": self.role_id,
            "party": base_serialize(self.party),
            "player": base_serialize(self.player),
            "role": base_serialize(self.role)
        }


@modules.utils.model
class Party(db.Model):
    __tablename__ = 'parties'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    title = db.Column(db.String(255), nullable=False)
    leader_id = db.Column(db.Integer, db.ForeignKey('players.id'))
    game = db.Column(db.String(64))
    max_players = db.Column(db.Integer)
    min_players = db.Column(db.Integer)
    description = db.Column(db.Text())
    channel_id = db.Column(db.Integer, db.ForeignKey('channels.id'))
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)

    channel = db.relationship('Channel')
    leader = db.relationship('Player')
    members = db.relationship('Member')

    swagger_metadata = {
        "id": {
            "type": int.__name__
        },
        "title": {
            "type": str.__name__
        },
        "leader_id": {
            "type": int.__name__
        },
        "game": {
            "type": str.__name__
        },
        "max_players": {
            "type": int.__name__
        },
        "min_players": {
            "type": int.__name__
        },
        "description": {
            "type": str.__name__,
        },
        "channel_id": {
            "type": int.__name__,
        },
        "start_time": {
            "type": datetime.datetime.__name__
        },
        "end_time": {
            "type": datetime.datetime.__name__
        },
        "channel": {
            "type": Channel.__name__
        },
        "leader": {
            "type": Player.__name__
        },
        "members": {
            "type": list.__name__
        }
    }

    def base_serialize(self):
        if self.start_time:
            start_time = datetime_to_string(self.start_time)
        else:
            start_time = self.start_time
        if self.end_time:
            end_time = datetime_to_string(self.end_time)
        else:
            end_time = self.end_time

        return {
            "id": self.id,
            "title": self.title,
            "leader_id": self.leader_id,
            "game": self.game,
            "max_players": self.max_players,
            "min_players": self.min_players,
            "description": self.description,
            "channel_id": self.channel_id,
            "start_time": start_time,
            "end_time": end_time,
        }

    def serialize(self):
        if self.start_time:
            start_time = datetime_to_string(self.start_time)
        else:
            start_time = self.start_time
        if self.end_time:
            end_time = datetime_to_string(self.end_time)
        else:
            end_time = self.end_time

        return {
            "id": self.id,
            "title": self.title,
            "leader_id": self.leader_id,
            "game": self.game,
            "max_players": self.max_players,
            "min_players": self.min_players,
            "description": self.description,
            "channel_id": self.channel_id,
            "start_time": start_time,
            "end_time": end_time,
            "channel": base_serialize(self.channel),
            "leader": base_serialize(self.leader),
            "members": list(map(lambda player: player.base_serialize(), self.members))
        }


@modules.utils.model
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    party_id = db.Column(db.Integer, db.ForeignKey('parties.id'))
    name = db.Column(db.String(64))
    max_players = db.Column(db.Integer)

    party = db.relationship('Party', backref=db.backref('roles', lazy=True))

    swagger_metadata = {
        "id": {
            "type": int.__name__
        },
        "party_id": {
            "type": int.__name__
        },
        "name": {
            "type": str.__name__
        },
        "max_players": {
            "type": int.__name__
        },
        "party": {
            "type": Party.__name__
        }
    }

    def base_serialize(self):
        return {
            "id": self.id,
            "party_id": self.party_id,
            "name": self.name,
            "max_players": self.max_players
        }

    def serialize(self):
        return {
            "id": self.id,
            "party_id": self.party_id,
            "name": self.name,
            "max_players": self.max_players,
            "party": base_serialize(self.party)
        }
