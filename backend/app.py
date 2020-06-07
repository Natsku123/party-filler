import logging
import os
import datetime
import requests
from flask import Flask, jsonify, request, url_for, redirect
from flask_restful import reqparse, abort, Api, Resource
from flask_migrate import Migrate
from flask_cors import CORS
from authlib.integrations.flask_client import OAuth

from modules.models import db, Player, Party, Role, Member, Server, Channel

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET')
oauth = OAuth()
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://{username}:{password}@{server}/{db}".format(
    username=os.environ.get("DB_USER"),
    password=os.environ.get("DB_PASS"),
    server="db",
    db=os.environ.get("DB_NAME")
)

oauth.init_app(app)
api = Api(app)
db.init_app(app)
migrate = Migrate(app, db)
CORS(app)

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
parser = reqparse.RequestParser()
parser.add_argument('party', help="Party object")
parser.add_argument('player', help="Player object")
parser.add_argument('server', help="Server object")
parser.add_argument('channel', help="Channel object")
parser.add_argument('member', help="Member object")
parser.add_argument('role', help="Role object")


class PartyResource(Resource):
    def get(self, party_id):
        return Party.query.filter_by(id=party_id).first().serialize()

    def delete(self, party_id):
        party = Party.query.filter_by(id=party_id).first()

        if party is None:
            abort(404)

        db.session.delete(party)
        db.session.commit()

        return {"status": "success"}

    def put(self, party_id):
        party = parser.parse_args().get('party')
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
    def get(self):
        return list(map(lambda party: party.serialize(), Party.query.order_by(Party.id.desc()).all()))

    def post(self):
        party = parser.parse_args().get('party')
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
    def get(self, page, per_page):
        return list(map(lambda party: party.serialize(), Party.query.order_by(Party.id.desc()).all().paginate(page, per_page)))


class ServerResource(Resource):
    def get(self, server_id):
        return Server.query.filter_by(id=server_id).first().serialize()

    def delete(self, server_id):
        server = Server.query.filter_by(id=server_id).first()

        if server is None:
            abort(404)

        db.session.delete(server)
        db.session.commit()

        return {"status": "success"}

    def put(self, server_id):
        server = parser.parse_args().get('server')
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
    def get(self):
        return list(map(lambda server: server.serialize(), Server.query.order_by(Party.id).all()))

    def post(self):
        server = parser.parse_args().get('server')

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
    def get(self, channel_id):
        return Channel.query.filter_by(id=channel_id).first().serialize()

    def delete(self, channel_id):
        channel = Channel.query.filter_by(id=channel_id).first()

        if channel is None:
            abort(404)

        db.session.delete(channel)
        db.session.commit()

        return {"status": "success"}

    def put(self, channel_id):
        channel = parser.parse_args().get('channel')
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
    def get(self, server_id):
        return list(map(lambda channel: channel.serialize(), Channel.filter_by(server_id=server_id).query.order_by(Party.id).all()))

    def post(self):
        channel = parser.parse_args().get('channel')

        if channel is None:
            abort(400)

        channel_obj = Channel(
            name=channel.get('name'),
            discord_id=channel.get('discord_id'),
            server_id=channel.get('server_id')
        )

        db.session.add(channel_obj)
        db.session.commit()

        return channel_obj.serialize()


class PlayerResource(Resource):
    def get(self, player_id):
        return Player.query.filter_by(id=player_id).first().serialize()

    def delete(self, player_id):
        player = Player.query.filter_by(id=player_id).first()

        if player is None:
            abort(404)

        db.session.delete(player)
        db.session.commit()

        return {"status": "success"}

    def put(self, player_id):
        player = parser.parse_args().get('player')
        player_obj = Player.query.filter_by(id=player_id).first()

        if player is None:
            abort(400)

        if player_obj is None:
            abort(404)

        if 'discord_id' in player:
            player_obj.discord_id = player.get('discord_id')

        db.session.commit()

        return player_obj.serialize()


class PlayerResources(Resource):
    def post(self):
        player = parser.parse_args().get('player')

        if player is None:
            abort(400)

        player_obj = Player(
            discord_id=player.get('discord_id')
        )

        db.session.add(player_obj)
        db.session.commit()

        return player_obj.serialize()


class MemberResource(Resource):
    def get(self, party_id, player_id):
        return Member.query.filter_by(party_id=party_id, player_id=player_id).first().serialize()

    def delete(self, party_id, player_id):
        member = Member.query.filter_by(party_id=party_id, player_id=player_id).first()

        if member is None:
            abort(404)

        db.session.delete(member)
        db.session.commit()

        return {"status": "success"}

    def put(self, party_id, player_id):
        member = parser.parse_args().get('member')
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
    def get(self, party_id):
        return None

    def post(self, party_id):
        member = parser.parse_args().get('member')
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


api.add_resource(PartyResource, '/parties/<party_id>')
api.add_resource(PartyResources, '/parties')
api.add_resource(PartyPageResource, '/parties/page/<page>/per/<per_page>')
api.add_resource(ServerResource, '/servers/<server_id>')
api.add_resource(ServerResources, '/servers')
api.add_resource(ChannelResource, '/channels/<channel_id>')
api.add_resource(ChannelResources, '/servers/<server_id>/channels')
api.add_resource(PlayerResource, '/players/<player_id>')
api.add_resource(PlayerResources, '/players')
api.add_resource(MemberResource, '/parties/<party_id>/players/<player_id>')
api.add_resource(MemberResources, '/parties/<party_id>/players')


@app.route('/login')
def login():
    redirect_uri = url_for('authorize', _external=True)
    return oauth.discord.authorize_redirect(redirect_uri)


@app.route('/authorize')
def authorize():
    # TODO do something with the token and profile
    token = oauth.discord.authorize_access_token()
    resp = oauth.discord.get('users/@me')
    profile = resp.json()
    logger.debug("Discord: " + str(profile))
    url = "http://" + os.environ.get('SITE_HOSTNAME')
    return redirect(url)


if __name__ == '__main___':
    app.run(debug=True)
