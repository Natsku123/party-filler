from sqlalchemy import Boolean, \
    Column, ForeignKey, Integer, String, Table, DateTime, Text
from sqlalchemy.orm import relationship, backref

from core import Base


player_server_association = Table(
    'players_servers',
    Base.metadata,
    Column('player_id', Integer, ForeignKey('players.id')),
    Column('server_id', Integer, ForeignKey('servers.id'))
)


class OAuth2Token(Base):
    __tablename__ = 'o_auth2_token'
    token_id = Column(Integer, primary_key=True, nullable=False)
    player_id = Column(Integer, ForeignKey('players.id'), nullable=False)
    name = Column(String(20), nullable=False)

    player = relationship('Player')

    token_type = Column(String(20))
    access_token = Column(String(48), nullable=False)
    refresh_token = Column(String(48))
    expires_at = Column(Integer, default=0)

    def to_token(self):
        return dict(
            access_token=self.access_token,
            token_type=self.token_type,
            refresh_token=self.refresh_token,
            expires_at=self.expires_at,
        )


class Server(Base):
    __tablename__ = 'servers'
    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String(255), nullable=False)
    icon = Column(String(64))
    discord_id = Column(String(64), nullable=False, unique=True)

    channels = relationship('Channel', backref=backref('server', lazy=True))
    players = relationship('Player', secondary=player_server_association, back_populates="servers")


class Channel(Base):
    __tablename__ = 'channels'
    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String(255), nullable=False)
    discord_id = Column(String(64), nullable=False, unique=True)
    server_id = Column(Integer, ForeignKey('servers.id'), nullable=False)


class Player(Base):
    __tablename__ = 'players'
    id = Column(Integer, primary_key=True, unique=True)
    discord_id = Column(String(64), nullable=False, unique=True)
    name = Column(String(64), nullable=False)
    discriminator = Column(String(4), nullable=False)
    icon = Column(String(64))

    servers = relationship('Server', secondary=player_server_association, back_populates="players")

    def dict(self):
        return {
            "id": self.id,
            "discord_id": self.discord_id,
            "name": self.name,
            "discriminator": self.discriminator,
            "icon": self.icon
        }


class Member(Base):
    __tablename__ = 'members'
    id = Column(Integer, primary_key=True, unique=True)
    player_req = Column(Integer)
    party_id = Column(Integer, ForeignKey('parties.id'), nullable=False)
    player_id = Column(Integer, ForeignKey('players.id'), nullable=False)
    role_id = Column(Integer, ForeignKey('roles.id'))

    party = relationship('Party', lazy="joined")
    player = relationship('Player', lazy="joined")
    role = relationship('Role', lazy="joined")


class Party(Base):
    __tablename__ = 'parties'
    id = Column(Integer, primary_key=True, unique=True)
    title = Column(String(255), nullable=False)
    leader_id = Column(Integer, ForeignKey('players.id'))
    game_id = Column(Integer, ForeignKey('games.id'))
    max_players = Column(Integer)
    min_players = Column(Integer)
    description = Column(Text())
    channel_id = Column(Integer, ForeignKey('channels.id'))
    start_time = Column(DateTime)
    end_time = Column(DateTime)

    channel = relationship('Channel', lazy="joined")
    leader = relationship('Player', lazy="joined")
    members = relationship('Member')
    game = relationship('Game', lazy="joined")


class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True, unique=True)
    party_id = Column(Integer, ForeignKey('parties.id'))
    name = Column(String(64))
    max_players = Column(Integer)

    party = relationship('Party', backref=backref('roles', lazy=True))


class Game(Base):
    __tablename__ = 'games'
    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String(255), nullable=False)
    default_max_players = Column(Integer)
