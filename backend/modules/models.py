from app import db


class Server(db.Model):
    __tablename__ = 'servers'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(255), nullable=False)
    discord_id = db.Column(db.String(64), nullable=False, unique=True)

    channels = db.relationship('Channel', backref='server', lazy=True)

    def base_serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "discord_id": self.discord_id
        }

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "discord_id": self.discord_id,
            "channels": list(map(lambda channel: channel.base_serialize(), self.channels))
        }


class Channel(db.Model):
    __tablename__ = 'channels'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(255), nullable=False)
    discord_id = db.Column(db.String(64), nullable=False, unique=True)
    server_id = db.Column(db.Integer, db.ForeignKey('server.id'), nullable=False)

    server = db.relationship('Server', backref=db.backref('servers', lazy=True))

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
            "server": self.server.base_serialize()
        }


class Player(db.Model):
    __tablename__ = 'players'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    discord_id = db.Column(db.String(64), nullable=False, unique=True)

    def base_serialize(self):
        return self.serialize()

    def serialize(self):
        return {
            "id": self.id,
            "discord_id": self.discord_id
        }


class Member(db.Model):
    __tablename__ = 'members'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    player_req = db.Column(db.Integer)
    party_id = db.Column(db.Integer, db.ForeignKey('parties'), nullable=False)
    player_id = db.Column(db.Integer, db.ForeignKey('players'), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles'))

    party = db.relationship('Party', backref=db.backref('parties', lazy=True))
    player = db.relationship('Player', backref=db.backref('players', lazy=True))
    role = db.relationship('Role', backref=db.backref('roles', lazy=True))

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
            "party": self.party.base_serialize(),
            "player": self.player.base_serialize(),
            "role": self.role.base_serialize()
        }


class Party(db.Model):
    __tablename__ = 'parties'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    title = db.Column(db.String(255), nullable=False)
    leader_id = db.Column(db.Integer, db.ForeignKey('players'))
    game = db.Column(db.String(64))
    max_players = db.Column(db.Integer)
    min_players = db.Column(db.Integer)
    description = db.Column(db.String(2000))
    channel_id = db.Column(db.Integer, db.ForeignKey('channels'))
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)

    channel = db.relationship('Channel', backref=db.backref('channels', lazy=True))
    leader = db.relationship('Player', backref=db.backref('players', lazy=True))
    players = db.relationship('Player', backref='party', lazy=True)

    def base_serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "leader_id": self.leader_id,
            "game": self.game,
            "max_players": self.max_players,
            "min_players": self.min_players,
            "description": self.description,
            "channel_id": self.channel_id,
            "start_time": self.start_time,
            "end_time": self.end_time,
        }

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "leader_id": self.leader_id,
            "game": self.game,
            "max_players": self.max_players,
            "min_players": self.min_players,
            "description": self.description,
            "channel_id": self.channel_id,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "channel": self.channel.base_serialize(),
            "leader": self.leader.base_serialize(),
            "players": list(map(lambda player: player.base_serialize(), self.players))
        }


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    party_id = db.Column(db.Integer, db.ForeignKey('parties'))
    name = db.Column(db.String(64))
    max_players = db.Column(db.Integer)

    party = db.relationship('Party', backref=db.backref('parties', lazy=True))

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
            "party": self.party.base_serialize()
        }
