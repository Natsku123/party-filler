import logging
import os
import datetime
from flask import Flask, jsonify, request, url_for, redirect, session
from flask_restful import reqparse, abort, Api, Resource
from flask_restful_swagger import swagger
from flask_migrate import Migrate
from flask_cors import CORS
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from authlib.integrations.flask_client import OAuth

from modules.models import db, Player, Party, Role, Member, Server, Channel, OAuth2Token

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET')
oauth = OAuth()
login_manager = LoginManager()
api = swagger.docs(Api(app), apiVersion='0.1')
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://{username}:{password}@{server}/{db}".format(
    username=os.environ.get("DB_USER"),
    password=os.environ.get("DB_PASS"),
    server="db",
    db=os.environ.get("DB_NAME")
)


@login_manager.user_loader
def load_user(player_id):
    return Player.query.filter_by(id=int(player_id)).first()


def update_token(name, token):
    token_obj = OAuth2Token.query.filter_by(name=name, player_id=current_user.id).first
    if not token_obj:
        token_obj = OAuth2Token(name=name, player_id=current_user.id)
    token_obj.token_type = token.get('token_type', 'bearer')
    token_obj.access_token = token.get('access_token')
    token_obj.refresh_token = token.get('refresh_token')
    token_obj.expires_at = token.get('expires_at')
    db.session.add(token_obj)
    db.session.commit()
    return token_obj


def fetch_discord_token():
    token = OAuth2Token.query.filter_by(name='twitter', player_id=current_user.id).first()
    if token:
        return token.to_token()


oauth.init_app(app, update_token=update_token)
db.init_app(app)
login_manager.init_app(app)
migrate = Migrate(app, db)
CORS(app, supports_credentials=True)

# OAuth with discord setup
oauth.register(
    name="discord",
    client_id=os.environ.get('DISCORD_CLIENT_ID'),
    client_secret=os.environ.get('DISCORD_CLIENT_SECRET'),
    access_token_url='https://discord.com/api/oauth2/token',
    access_token_params=None,
    authorize_url='https://discord.com/api/oauth2/authorize',
    authorize_params=None,
    api_base_url='https://discord.com/api/v6',
    client_kwargs={'scope': 'identify guilds'}
)


# Logger
logger = logging.getLogger('api')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# TODO more arguments as things are created
# parser = reqparse.RequestParser()
# parser.add_argument('party', help="Party object")
# parser.add_argument('player', help="Player object")
# parser.add_argument('server', help="Server object")
# parser.add_argument('channel', help="Channel object")
# parser.add_argument('member', help="Member object")
# parser.add_argument('role', help="Role object")


class PartyResource(Resource):
    method_decorators = {
        'delete': [login_required],
        'put': [login_required]
    }

    @swagger.operation(
        notes='Get a party based on party ID.',
        responseClass=Party.__name__,
        responseMessages=[
            {
                "code": 404,
                "message": "Party not found."
            }
        ],
        parameters=[
            {
                "dataType": int.__name__,
                "required": True,
                "name": "party_id"
            }
        ]
    )
    def get(self, party_id):
        party = Party.query.filter_by(id=party_id).first()

        if party is None:
            abort(404)

        return party.serialize()

    @swagger.operation(
        notes='Delete a party based on party ID.',
        responseMessages=[
            {
                "code": 404,
                "message": "Party not found."
            }
        ],
        parameters=[
            {
                "dataType": int.__name__,
                "required": True,
                "name": "party_id"
            }
        ]
    )
    def delete(self, party_id):
        party = Party.query.filter_by(id=party_id).first()

        if party is None:
            abort(404)

        db.session.delete(party)
        db.session.commit()

        return {"status": "success"}

    @swagger.operation(
        notes='Edit a party based on party ID.',
        responseClass=Party.__name__,
        responseMessages=[
            {
                "code": 400,
                "message": "Party object not found as input."
            },
            {
                "code": 404,
                "message": "Party not found."
            }
        ],
        parameters=[
            {
                "dataType": int.__name__,
                "required": True,
                "name": "party_id"
            },
            {
                "dataType": Party.__name__,
                "required": True,
                "name": "party"
            }
        ]
    )
    def put(self, party_id):
        party = request.get_json().get('party')
        party_obj = Party.query.filter_by(id=party_id).first()

        if party is None:
            abort(400)

        if party_obj is None:
            abort(404)

        if 'title' in party:
            party_obj.title = party.get('title')
        if 'leader_id' in party:
            party_obj.leader_id = party.get('leader_id')
        if 'game' in party:
            party_obj.game = party.get('game')
        if 'max_players' in party:
            party_obj.max_players = party.get('max_players')
        if 'min_players' in party:
            party_obj.min_players = party.get('min_players')
        if 'description' in party:
            party_obj.description = party.get('description')
        if 'channel_id' in party:
            party_obj.channel_id = party.get('channel_id')
        if 'start_time' in party:
            party_obj.start_time = party.get('start_time')
        if 'end_time' in party:
            party_obj.end_time = party.get('end_time')

        db.session.commit()

        return party_obj.serialize()


class PartyResources(Resource):
    method_decorators = {
        'post': [login_required]
    }

    @swagger.operation(
        notes='Get list of parties.',
        responseClass=Party.__name__
    )
    def get(self):
        return list(map(lambda party: party.serialize(), Party.query.order_by(Party.id.desc()).all()))

    @swagger.operation(
        notes='Create a party',
        responseClass=Party.__name__,
        responseMessages=[
            {
                "code": 400,
                "message": "Party object not found as input."
            }
        ],
        parameters=[
            {
                "dataType": Party.__name__,
                "required": True,
                "name": "party"
            }
        ]
    )
    def post(self):
        party = request.get_json().get('party')
        if party is None:
            abort(400)

        if 'start_time' in party and party['start_time'] is not None:
            party['start_time'] = datetime.datetime.fromisoformat(party['start_time'])

        if 'end_time' in party and party['end_time'] is not None:
            party['end_time'] = datetime.datetime.fromisoformat(party['end_time'])

        party_obj = Party(
            title=party.get('title'),
            leader_id=party.get('leader_id'),
            game=party.get('game'),
            max_players=party.get('max_players'),
            min_players=party.get('min_players'),
            description=party.get('description'),
            channel_id=party.get('channel_id'),
            start_time=party.get('start_time'),
            end_time=party.get('end_time')
        )

        db.session.add(party_obj)
        db.session.commit()

        return party_obj.serialize()


class PartyPageResource(Resource):

    @swagger.operation(
        notes='Get list of parties with pagination.',
        responseClass=Party.__name__,
        parameters=[
            {
                "dataType": int.__name__,
                "required": True,
                "name": "page"
            },
            {
                "dataType": int.__name__,
                "required": True,
                "name": "per_page"
            }
        ]
    )
    def get(self, page, per_page):
        return list(map(lambda party: party.serialize(), Party.query.order_by(Party.id.desc()).all().paginate(page, per_page)))


class ServerResource(Resource):
    method_decorators = {
        'delete': [login_required],
        'put': [login_required]
    }

    @swagger.operation(
        notes='Get server based on server ID.',
        responseClass=Server.__name__,
        responseMessages=[
            {
                "code": 404,
                "message": "Server not found."
            }
        ],
        parameters=[
            {
                "dataType": int.__name__,
                "required": True,
                "name": "server_id"
            }
        ]
    )
    def get(self, server_id):
        server = Server.query.filter_by(id=server_id).first()

        if server is None:
            abort(404)

        return server.serialize()

    @swagger.operation(
        notes='Delete server based on server ID.',
        responseMessages=[
            {
                "code": 404,
                "message": "Server not found."
            }
        ],
        parameters=[
            {
                "dataType": int.__name__,
                "required": True,
                "name": "server_id"
            }
        ]
    )
    def delete(self, server_id):
        server = Server.query.filter_by(id=server_id).first()

        if server is None:
            abort(404)

        db.session.delete(server)
        db.session.commit()

        return {"status": "success"}

    @swagger.operation(
        notes='Edit server based on server ID.',
        responseClass=Server.__name__,
        responseMessages=[
            {
                "code": 400,
                "message": "Server object not found as input."
            },
            {
                "code": 404,
                "message": "Server not found."
            }
        ],
        parameters=[
            {
                "dataType": int.__name__,
                "required": True,
                "name": "server_id"
            },
            {
                "dataType": Server.__name__,
                "required": True,
                "name": "server"
            }
        ]
    )
    def put(self, server_id):
        server = request.get_json().get('server')
        server_obj = Server.query.filter_by(id=server_id).first()

        if server is None:
            abort(400)

        if server_obj is None:
            abort(404)

        if 'name' in server:
            server_obj.name = server.get('name')
        if 'discord_id' in server:
            server_obj.discord_id = server.get('discord_id')

        db.session.commit()

        return server_obj.serialize()


class ServerResources(Resource):
    method_decorators = {
        'post': [login_required]
    }

    @swagger.operation(
        notes='Get list of servers',
        responseClass=Server.__name__
    )
    def get(self):
        return list(map(lambda server: server.serialize(), Server.query.order_by(Server.id).all()))

    @swagger.operation(
        notes='Create a server.',
        responseClass=Server.__name__,
        responseMessages=[
            {
                "code": 400,
                "message": "Server object not found as input."
            }
        ],
        parameters=[
            {
                "dataType": Server.__name__,
                "required": True,
                "name": "server"
            }
        ]
    )
    def post(self):
        server = request.get_json().get('server')

        if server is None:
            abort(400)

        server_obj = Server(
            name=server.get('name'),
            discord_id=server.get('discord_id')
        )

        db.session.add(server_obj)
        db.session.commit()

        return server_obj.serialize()


class ChannelResource(Resource):
    method_decorators = {
        'delete': [login_required],
        'put': [login_required]
    }

    @swagger.operation(
        notes='Get a channel based on channel ID.',
        responseClass=Channel.__name__,
        responseMessages=[
            {
                "code": 404,
                "message": "Channel not found."
            }
        ],
        parameters=[
            {
                "dataType": int.__name__,
                "required": True,
                "name": "channel_id"
            }
        ]
    )
    def get(self, channel_id):
        channel = Channel.query.filter_by(id=channel_id).first()

        if channel is None:
            abort(404)

        return channel.serialize()

    @swagger.operation(
        notes='Delete channel based on channel ID.',
        responseMessages=[
            {
                "code": 404,
                "message": "Channel not found."
            }
        ],
        parameters=[
            {
                "dataType": int.__name__,
                "required": True,
                "name": "channel_id"
            }
        ]
    )
    def delete(self, channel_id):
        channel = Channel.query.filter_by(id=channel_id).first()

        if channel is None:
            abort(404)

        db.session.delete(channel)
        db.session.commit()

        return {"status": "success"}

    @swagger.operation(
        notes='Edit channel based on channel ID.',
        responseClass=Channel.__name__,
        responseMessages=[
            {
                "code": 400,
                "message": "Channel object not found as input."
            },
            {
                "code": 404,
                "message": "Channel not found."
            }
        ],
        parameters=[
            {
                "dataType": int.__name__,
                "required": True,
                "name": "channel_id"
            },
            {
                "dataType": Channel.__name__,
                "required": True,
                "name": "channel"
            }
        ]
    )
    def put(self, channel_id):
        channel = request.get_json().get('channel')
        channel_obj = Channel.query.filter_by(id=channel_id).first()

        if channel is None:
            abort(400)

        if channel_obj is None:
            abort(404)

        if 'name' in channel:
            channel_obj.name = channel.get('name')
        if 'discord_id' in channel:
            channel_obj.discord_id = channel.get('discord_id')
        if 'server_id' in channel:
            channel_obj.server_id = channel.get('server_id')

        db.session.commit()

        return channel_obj.serialize()


class ChannelResources(Resource):

    @swagger.operation(
        notes='Get list of channels on a server.',
        responseClass=Channel.__name__,
        parameters=[
            {
                "dataType": int.__name__,
                "required": True,
                "name": "server_id"
            }
        ]
    )
    def get(self, server_id):
        return list(map(lambda channel: channel.serialize(), Channel.query.filter_by(server_id=server_id).order_by(Party.id).all()))

    @swagger.operation(
        notes='Add a channel to a server.',
        responseClass=Channel.__name__,
        responseMessages=[
            {
                "code": 400,
                "message": "Channel object not found as input."
            },
            {
                "code": 404,
                "message": "Server not found."
            }
        ],
        parameters=[
            {
                "dataType": int.__name__,
                "required": True,
                "name": "server_id"
            },
            {
                "dataType": Party.__name__,
                "required": True,
                "name": "channel"
            }
        ]
    )
    def post(self, server_id):
        channel = request.get_json().get('channel')

        server = Server.query.filter_by(server_id=server_id).first()
        if server is None:
            abort(404)

        if channel is None:
            abort(400)

        channel_obj = Channel(
            name=channel.get('name'),
            discord_id=channel.get('discord_id'),
            server_id=channel.get('server_id')
        )

        server.channels.append(channel_obj)
        db.session.add(channel_obj)
        db.session.commit()

        return channel_obj.serialize()


class PlayerResource(Resource):
    method_decorators = {
        'delete': [login_required],
        'put': [login_required]
    }

    @swagger.operation(
        notes='Get player based on player ID.',
        responseClass=Player.__name__,
        responseMessages=[
            {
                "code": 404,
                "message": "Player not found."
            }
        ],
        parameters=[
            {
                "dataType": int.__name__,
                "required": True,
                "name": "player_id"
            }
        ]
    )
    def get(self, player_id):
        player = Player.query.filter_by(id=player_id).first()

        if player is None:
            abort(404)

        return player.serialize()

    @swagger.operation(
        notes='Delete player based on player ID.',
        responseMessages=[
            {
                "code": 404,
                "message": "Player not found."
            }
        ],
        parameters=[
            {
                "dataType": int.__name__,
                "required": True,
                "name": "player_id"
            }
        ]
    )
    def delete(self, player_id):
        player = Player.query.filter_by(id=player_id).first()

        if player is None:
            abort(404)

        db.session.delete(player)
        db.session.commit()

        return {"status": "success"}

    @swagger.operation(
        notes='Edit player based on player ID.',
        responseClass=Player.__name__,
        responseMessages=[
            {
                "code": 400,
                "message": "Player object not found as input."
            },
            {
                "code": 404,
                "message": "Player not found."
            }
        ],
        parameters=[
            {
                "dataType": int.__name__,
                "required": True,
                "name": "player_id"
            },
            {
                "dataType": Player.__name__,
                "required": True,
                "name": "player"
            }
        ]
    )
    def put(self, player_id):
        player = request.get_json().get('player')
        player_obj = Player.query.filter_by(id=player_id).first()

        if player is None:
            abort(400)

        if player_obj is None:
            abort(404)

        if 'discord_id' in player:
            player_obj.discord_id = player.get('discord_id')

        db.session.commit()

        return player_obj.serialize()


class MemberResource(Resource):
    method_decorators = {
        'delete': [login_required],
        'put': [login_required]
    }

    @swagger.operation(
        notes='Get member with party ID and player ID.',
        responseClass=Member.__name__,
        responseMessages=[
            {
                "code": 404,
                "message": "Member not found."
            }
        ],
        parameters=[
            {
                "dataType": int.__name__,
                "required": True,
                "name": "party_id"
            },
            {
                "dataType": int.__name__,
                "required": True,
                "name": "player_id"
            }
        ]
    )
    def get(self, party_id, player_id):
        member = Member.query.filter_by(party_id=party_id, player_id=player_id).first()

        if member is None:
            abort(404)

        return member.serialize()

    @swagger.operation(
        notes='Delete member with party ID and player ID.',
        responseMessages=[
            {
                "code": 404,
                "message": "Member not found."
            }
        ],
        parameters=[
            {
                "dataType": int.__name__,
                "required": True,
                "name": "party_id"
            },
            {
                "dataType": int.__name__,
                "required": True,
                "name": "player_id"
            }
        ]
    )
    def delete(self, party_id, player_id):
        member = Member.query.filter_by(party_id=party_id, player_id=player_id).first()

        if member is None:
            abort(404)

        db.session.delete(member)
        db.session.commit()

        return {"status": "success"}

    @swagger.operation(
        notes='Edit member with party ID and player ID.',
        responseClass=Member.__name__,
        responseMessages=[
            {
                "code": 400,
                "message": "Member object not found as input."
            },
            {
                "code": 404,
                "message": "Member not found."
            }
        ],
        parameters=[
            {
                "dataType": int.__name__,
                "required": True,
                "name": "party_id"
            },
            {
                "dataType": int.__name__,
                "required": True,
                "name": "player_id"
            },
            {
                "dataType": Member.__name__,
                "required": True,
                "name": "member"
            }
        ]
    )
    def put(self, party_id, player_id):
        member = request.get_json().get('member')
        member_obj = Member.query.filter_by(party_id=party_id, player_id=player_id).first()

        if member is None:
            abort(400)

        if member_obj is None:
            abort(404)

        if 'player_req' in member:
            member_obj.player_req = member.get('player_req')
        if 'party_id' in member:
            member_obj.party_id = member.get('party_id')
        if 'player_id' in member:
            member_obj.player_id = member.get('player_id')
        if 'role_id' in member:
            member_obj.role_id = member.get('role_id')

        db.session.commit()

        return member_obj.serialize()


class MemberResources(Resource):
    method_decorators = {
        'post': [login_required]
    }

    @swagger.operation(
        notes='Get lsit of member is party.',
        responseClass=Member.__name__,
        parameters=[
            {
                "dataType": int.__name__,
                "required": True,
                "name": "party_id"
            }
        ]
    )
    def get(self, party_id):
        return list(map(lambda member: member.serialize(), Member.query.filter_by(party_id=party_id).order_by(Member.id).all()))

    @swagger.operation(
        notes='Create a new member into a party.',
        responseClass=Member.__name__,
        responseMessages=[
            {
                "code": 400,
                "message": "Member object not found as input."
            },
            {
                "code": 404,
                "message": "Party not found."
            }
        ],
        parameters=[
            {
                "dataType": int.__name__,
                "required": True,
                "name": "party_id"
            },
            {
                "dataType": Member.__name__,
                "required": True,
                "name": "member"
            }
        ]
    )
    def post(self, party_id):
        member = request.get_json().get('member')
        party = Party.query.filter_by(id=party_id).first()

        if member is None:
            abort(400)

        if party is None:
            abort(404)

        member_obj = Member(
            party_req=member.get('party_req'),
            party_id=member.get('party_id'),
            player_id=member.get('player_id'),
            role_id=member.get('role_id')
        )

        db.session.add(member_obj)
        db.session.commit()

        return member_obj.serialize()


class RoleResource(Resource):
    method_decorators = {
        'delete': [login_required],
        'put': [login_required]
    }

    @swagger.operation(
        notes='Get role with role ID.',
        responseClass=Role.__name__,
        responseMessages=[
            {
                "code": 404,
                "message": "Role not found."
            }
        ],
        parameters=[
            {
                "dataType": int.__name__,
                "required": True,
                "name": "role_id"
            }
        ]
    )
    def get(self, role_id):
        role = Role.query.filter_by(id=role_id).first()

        if role is None:
            abort(404)

        return role.serialize()

    @swagger.operation(
        notes='Delete role with role ID.',
        responseMessages=[
            {
                "code": 404,
                "message": "Role not found."
            }
        ],
        parameters=[
            {
                "dataType": int.__name__,
                "required": True,
                "name": "role_id"
            }
        ]
    )
    def delete(self, role_id):
        role = Role.query.filter_by(id=role_id).first()

        if role is None:
            abort(404)

        db.session.delete(role)
        db.session.commit()

        return {"status": "success"}

    @swagger.operation(
        notes='Edit role with role ID.',
        responseClass=Role.__name__,
        responseMessages=[
            {
                "code": 400,
                "message": "Role object not found as input."
            },
            {
                "code": 404,
                "message": "Role not found."
            }
        ],
        parameters=[
            {
                "dataType": int.__name__,
                "required": True,
                "name": "role_id"
            },
            {
                "dataType": Role.__name__,
                "required": True,
                "name": "role"
            }
        ]
    )
    def put(self, role_id):
        role = request.get_json().get('role')
        role_obj = Role.query.filter_by(id=role_id).first()

        if role is None:
            abort(400)

        if role_obj is None:
            abort(404)

        role_obj.party_id = role.get('party_id')
        role_obj.name = role.get('name')
        role_obj.max_players = role.get('max_players')
        db.session.commit()
        return role_obj.serialize()


class RoleResources(Resource):
    method_decorators = {
        'post': [login_required]
    }

    @swagger.operation(
        notes='Get list of roles in party.',
        responseClass=Role.__name__,
        parameters=[
            {
                "dataType": int.__name__,
                "required": True,
                "name": "party_id"
            }
        ]
    )
    def get(self, party_id):
        return list(map(lambda role: role.serialize(), Role.query.filter_by(party_id=party_id).order_by(Role.id).all()))

    @swagger.operation(
        notes='Edit player based on player ID.',
        responseClass=Role.__name__,
        responseMessages=[
            {
                "code": 400,
                "message": "Role object not found as input."
            },
            {
                "code": 404,
                "message": "Party not found."
            }
        ],
        parameters=[
            {
                "dataType": int.__name__,
                "required": True,
                "name": "party_id"
            },
            {
                "dataType": Role.__name__,
                "required": True,
                "name": "role"
            }
        ]
    )
    def post(self, party_id):
        role = request.get_json().get('role')
        party = Party.query.filter_by(id=party_id).first()

        if role is None:
            abort(400)

        if party is None:
            abort(404)

        role_obj = Role(
            party_id=party_id,
            name=role.get('name'),
            max_players=role.get('max_players')
        )

        db.session.add(role_obj)
        db.session.commit()

        return role_obj.serialize()


api.add_resource(PartyResource, '/parties/<int:party_id>')
api.add_resource(PartyResources, '/parties')
api.add_resource(PartyPageResource, '/parties/page/<int:page>/per/<int:per_page>')
api.add_resource(ServerResource, '/servers/<int:server_id>')
api.add_resource(ServerResources, '/servers')
api.add_resource(ChannelResource, '/channels/<int:channel_id>')
api.add_resource(ChannelResources, '/servers/<int:server_id>/channels')
api.add_resource(PlayerResource, '/players/<int:player_id>')
api.add_resource(MemberResource, '/parties/<int:party_id>/players/<int:player_id>')
api.add_resource(MemberResources, '/parties/<int:party_id>/players')
api.add_resource(RoleResource, '/roles/<int:role_id>')
api.add_resource(RoleResources, '/parties/<int:party_id>/roles')


@app.route('/login')
def login():
    redirect_uri = url_for('authorize', _external=True)

    redirect_url = request.args.get('redirect')
    if redirect_url is None:
        redirect_url = "http://" + os.environ.get('SITE_HOSTNAME')

    session['redirect_url'] = redirect_url

    return oauth.discord.authorize_redirect(redirect_uri)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    redirect_url = "http://" + os.environ.get('SITE_HOSTNAME')
    return redirect(redirect_url)


@app.route('/authorize')
def authorize():
    token = oauth.discord.authorize_access_token()
    resp = oauth.discord.get('users/@me')
    profile = resp.json()

    url = session.get('redirect_url')
    if url is None:
        url = "http://" + os.environ.get('SITE_HOSTNAME')
    else:
        del session['redirect_url']

    # Get player
    player = Player.query.filter_by(discord_id=profile['id']).first()

    # If player doesn't exist, create a new one.
    if player is None:
        logger.debug("Player object" + str(profile))
        player = Player(
            discord_id=profile.get('id'),
            name=profile.get('username'),
            icon=profile.get('avatar'),
            is_authenticated=True
        )

        # Get servers that Player uses
        guilds = oauth.discord.get('users/@me/guilds')

        # Create new servers if doesn't already exist
        for guild in guilds.json():
            server = Server.query.filter_by(discord_id=guild['id']).first()
            if server is None:
                server = Server(
                    name=guild.get('name'),
                    icon=guild.get('icon'),
                    discord_id=guild.get('id')
                )

                # Link server to player
                player.servers.append(server)
                db.session.add(server)

        db.session.add(player)

    # Update token
    token_obj = OAuth2Token.query.filter_by(player_id=player.id).first()
    if token_obj is None:
        token_obj = OAuth2Token(
            player_id=player.id,
            name='discord',
            token_type=token.get('token_type'),
            access_token=token.get('access_token'),
            refresh_token=token.get('refresh_token'),
            expires_at=token.get('expires_at')
        )
    else:
        token_obj.token_type = token.get('token_type'),
        token_obj.access_token = token.get('access_token'),
        token_obj.refresh_token = token.get('refresh_token'),
        token_obj.expires_at = token.get('expires_at')

    db.session.add(token_obj)
    db.session.commit()

    login_user(player)

    return redirect(url)


if __name__ == '__main___':
    app.run(debug=True)
