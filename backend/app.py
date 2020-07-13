import logging
import os
import datetime
import dateutil.parser
from flask import Flask, jsonify, request, url_for, redirect, session
from flask_restful import reqparse, abort, Api, Resource
from flask_restful_swagger import swagger
from flask_migrate import Migrate
from flask_cors import CORS
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from authlib.integrations.flask_client import OAuth

from modules.models import db, Player, Party, Role, Member, Server, Channel, OAuth2Token
from modules.utils import custom_get, custom_check, snake_dict_to_camel, send_webhook

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
    token_obj = OAuth2Token.query.filter_by(name=name, player_id=current_user.id).first()
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
    token = OAuth2Token.query.filter_by(name='discord', player_id=current_user.id).first()
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
    client_kwargs={'scope': 'identify guilds'},
    fetch_token=fetch_discord_token
)


# Logger
logger = logging.getLogger('api')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# TODO more arguments as things are created
parser = reqparse.RequestParser()
# parser.add_argument('party', help="Party object")
# parser.add_argument('player', help="Player object")
# parser.add_argument('server', help="Server object")
# parser.add_argument('channel', help="Channel object")
# parser.add_argument('member', help="Member object")
# parser.add_argument('role', help="Role object")
parser.add_argument('camel', help="Use camelCase instead of snake_case")


def check_camel(func):
    def wrapper(*args, **kwargs):
        return_value = func(*args, **kwargs)
        if 'camel' in parser.parse_args() and \
                (isinstance(return_value, dict) or
                 isinstance(return_value, list)):
            return snake_dict_to_camel(return_value)
        return return_value
    return wrapper


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
    @check_camel
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
    @check_camel
    def delete(self, party_id):
        party = Party.query.filter_by(id=party_id).first()

        if party is None:
            abort(404)

        if party.leader_id != current_user.id:
            return login_manager.unauthorized()

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
    @check_camel
    def put(self, party_id):
        party = custom_get(request.get_json(), 'party')
        party_obj = Party.query.filter_by(id=party_id).first()

        if party is None:
            abort(400)

        if party_obj is None:
            abort(404)

        if party_obj.leader_id != current_user.id:
            abort(401)

        if custom_check(party, 'title'):
            party_obj.title = custom_get(party, 'title')
        if custom_check(party, 'leader_id'):
            party_obj.leader_id = custom_get(party, 'leader_id')
        if custom_check(party, 'game'):
            party_obj.game = custom_get(party, 'game')
        if custom_check(party, 'max_players'):
            party_obj.max_players = custom_get(party, 'max_players')
        if custom_check(party, 'min_players'):
            party_obj.min_players = custom_get(party, 'min_players')
        if custom_check(party, 'description'):
            party_obj.description = custom_get(party, 'description')
        if custom_check(party, 'channel_id'):
            party_obj.channel_id = custom_get(party, 'channel_id')
        if custom_check(party, 'start_time'):
            party_obj.start_time = custom_get(party, 'start_time')
        if custom_check(party, 'end_time'):
            party_obj.end_time = custom_get(party, 'end_time')

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
    @check_camel
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
    @check_camel
    def post(self):
        party = custom_get(request.get_json(), 'party')
        if party is None:
            abort(400)

        start_time = custom_get(party, 'start_time')
        end_time = custom_get(party, 'end_time')

        if start_time is not None:
            party['start_time'] = dateutil.parser.parse(start_time)

        if end_time is not None:
            party['end_time'] = dateutil.parser.parse(end_time)

        party_obj = Party(
            title=custom_get(party, 'title'),
            leader_id=custom_get(party, 'leader_id'),
            game=custom_get(party, 'game'),
            max_players=custom_get(party, 'max_players'),
            min_players=custom_get(party, 'min_players'),
            description=custom_get(party, 'description'),
            channel_id=custom_get(party, 'channel_id'),
            start_time=custom_get(party, 'start_time'),
            end_time=custom_get(party, 'end_time')
        )

        db.session.add(party_obj)
        db.session.commit()

        if party_obj.channel:
            send_webhook(party_obj.serialize())

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
    @check_camel
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
    @check_camel
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
    @check_camel
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
    @check_camel
    def put(self, server_id):
        server = custom_get(request.get_json(), 'server')
        server_obj = Server.query.filter_by(id=server_id).first()

        if server is None:
            abort(400)

        if server_obj is None:
            abort(404)

        if custom_check(server, 'name'):
            server_obj.name = custom_get(server, 'name')
        if custom_check(server, 'discord_id'):
            server_obj.discord_id = custom_get(server, 'discord_id')

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
    @check_camel
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
    @check_camel
    def post(self):
        server = custom_get(request.get_json(), 'server')

        if server is None:
            abort(400)

        server_obj = Server(
            name=custom_get(server, 'name'),
            discord_id=custom_get(server, 'discord_id')
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
    @check_camel
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
    @check_camel
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
    @check_camel
    def put(self, channel_id):
        channel = custom_get(request.get_json(), 'channel')
        channel_obj = Channel.query.filter_by(id=channel_id).first()

        if channel is None:
            abort(400)

        if channel_obj is None:
            abort(404)

        if custom_check(channel, 'name'):
            channel_obj.name = custom_get(channel, 'name')
        if custom_check(channel, 'discord_id'):
            channel_obj.discord_id = custom_get(channel, 'discord_id')
        if custom_check(channel, 'server_id'):
            channel_obj.server_id = custom_get(channel, 'server_id')

        db.session.commit()

        return channel_obj.serialize()


class ChannelResources(Resource):
    method_decorators = {
        'post': [login_required],
    }
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
    @check_camel
    def post(self):
        channel = custom_get(request.get_json(), 'channel')

        token = OAuth2Token.query.filter_by(name='discord', player_id=current_user.id).first()

        if token is None:
            return login_manager.unauthorized()

        channel_dc = oauth.discord.get(
            'channels/{:}'.format(custom_get(channel, 'discord_id')),
            token=token.to_token()
        ).json()

        logger.debug(channel_dc)

        if 'code' in channel_dc:
            logger.error("Discord Error: " + str(channel_dc['code']) + " " + str(channel_dc['message']))
            abort(400)

        if channel is None or channel_dc is None:
            abort(400)

        server = Server.query.filter_by(discord_id=str(channel_dc.get('guild_id'))).first()
        if server is None:
            abort(404)

        channel_obj = Channel(
            name=custom_get(channel_dc, 'name'),
            discord_id=custom_get(channel, 'discord_id'),
            server_id=server.id
        )

        server.channels.append(channel_obj)
        db.session.add(channel_obj)
        db.session.commit()

        return channel_obj.serialize()


class ServerChannelResources(Resource):

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
    @check_camel
    def get(self, server_id):
        return list(map(lambda channel: channel.serialize(), Channel.query.filter_by(server_id=server_id).order_by(Party.id).all()))


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
    @check_camel
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
    @check_camel
    def delete(self, player_id):
        if player_id != current_user.id:
            return login_manager.unauthorized()

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
    @check_camel
    def put(self, player_id):
        if player_id != current_user.id:
            return login_manager.unauthorized()

        player = custom_get(request.get_json(), 'player')
        player_obj = Player.query.filter_by(id=player_id).first()

        if player is None:
            abort(400)

        if player_obj is None:
            abort(404)

        if custom_check(player, 'discord_id'):
            player_obj.discord_id = custom_get(player, 'discord_id')

        db.session.commit()

        return player_obj.serialize()


class PlayerResources(Resource):
    method_decorators = {
        'get': [login_required],
    }

    @swagger.operation(
        notes='Get current player',
        responseClass=Player.__name__,
        responseMessages=[
            {
                "code": 404,
                "message": "Player not found."
            }
        ]
    )
    @check_camel
    def get(self):
        player = Player.query.filter_by(id=current_user.id).first()

        if player is None:
            abort(404)

        return player.serialize()


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
    @check_camel
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
    @check_camel
    def delete(self, party_id, player_id):
        member = Member.query.filter_by(party_id=party_id, player_id=player_id).first()

        if member.party.leader_id != current_user.id and player_id != current_user.id:
            return login_manager.unauthorized()
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
    @check_camel
    def put(self, party_id, player_id):
        if current_user.id != player_id:
            return login_manager.unauthorized()

        member = custom_get(request.get_json(), 'member')
        member_obj = Member.query.filter_by(party_id=party_id, player_id=player_id).first()

        if member is None:
            abort(400)

        if member_obj is None:
            abort(404)

        if custom_check(member, 'player_req'):
            member_obj.player_req = custom_get(member, 'player_req')
        if custom_check(member, 'party_id'):
            member_obj.party_id = custom_get(member, 'party_id')
        if custom_check(member, 'player_id'):
            member_obj.player_id = custom_get(member, 'player_id')
        if custom_check(member, 'role_id'):
            member_obj.role_id = custom_get(member, 'role_id')

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
    @check_camel
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
    @check_camel
    def post(self, party_id):
        member = custom_get(request.get_json(), 'member')
        party = Party.query.filter_by(id=party_id).first()

        if member is None:
            abort(400)

        if party is None:
            abort(404)

        member_obj = Member(
            player_req=custom_get(member, 'player_req'),
            party_id=custom_get(member, 'party_id'),
            player_id=custom_get(member, 'player_id'),
            role_id=custom_get(member, 'role_id')
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
    @check_camel
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
    @check_camel
    def delete(self, role_id):
        role = Role.query.filter_by(id=role_id).first()

        if role is None:
            abort(404)

        if role.party.leader_id != current_user.id:
            return login_manager.unauthorized()

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
    @check_camel
    def put(self, role_id):
        role = custom_get(request.get_json(), 'role')
        role_obj = Role.query.filter_by(id=role_id).first()

        if role is None:
            abort(400)

        if role_obj is None:
            abort(404)

        if role_obj.party.leader_id != current_user.id:
            return login_manager.unauthorized()

        role_obj.party_id = custom_get(role, 'party_id')
        role_obj.name = custom_get(role, 'name')
        role_obj.max_players = custom_get(role, 'max_players')
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
    @check_camel
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
    @check_camel
    def post(self, party_id):
        role = custom_get(request.get_json(), 'role')
        party = Party.query.filter_by(id=party_id).first()

        if role is None:
            abort(400)

        if party is None:
            abort(404)

        if party.leader_id != current_user.id:
            return login_manager.unauthorized()

        role_obj = Role(
            party_id=party_id,
            name=custom_get(role, 'name'),
            max_players=custom_get(role, 'max_players')
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
api.add_resource(ChannelResources, '/channels')
api.add_resource(ServerChannelResources, '/servers/<int:server_id>/channels')
api.add_resource(PlayerResource, '/players/<int:player_id>')
api.add_resource(PlayerResources, '/players')
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


@app.route('/add_bot')
def add_bot():
    return redirect("https://discord.com/api/oauth2/authorize?client_id=718047907617439804&permissions=0&redirect_uri=http%3A%2F%2Fparty.hellshade.fi%2F&scope=bot")


if __name__ == '__main___':
    app.run(debug=True)
