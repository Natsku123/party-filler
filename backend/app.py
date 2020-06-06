import logging
import os
import datetime
from flask import Flask, jsonify, request
from flask_restful import reqparse, abort, Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from modules.models import Player, Party, Role, Member, Server, Channel

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://{username}:{password}@{server}/{db}".format(
    username=os.environ.get("DB_USER"),
    password=os.environ.get("DB_PASS"),
    server="db",
    db=os.environ.get("DB_NAME")
)
api = Api(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


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


class PartyResources(Resource):
    def get(self):
        return list(map(lambda party: party.serialize(), Party.query.order_by(Party.id.desc()).all()))


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
            server_obj.leader_id = server.get('name')
        if 'discord_id' in server:
            server_obj.game = server.get('discord_id')

        db.session.commit()

        return server_obj.serialize()

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


class ServerResources(Resource):
    def get(self):
        return list(map(lambda server: server.serialize(), Server.query.order_by(Party.id).all()))


class ChannelResource(Resource):
    def get(self, channel_id):
        return Channel.query.filter_by(id=channel_id).first().serialize()

    def post(self):
        return None


class ChannelResources(Resource):
    def get(self, server_id):
        return list(map(lambda channel: channel.serialize(), Channel.filter_by(server_id=server_id).query.order_by(Party.id).all()))


api.add_resource(PartyResource, '/parties/<party_id>')
api.add_resource(PartyResources, '/parties')
api.add_resource(PartyPageResource, '/parties/page/<page>/per/<per_page>')
api.add_resource(ServerResource, '/servers/<server_id>')
api.add_resource(ServerResources, '/servers')
api.add_resource(ChannelResource, '/channels/<channel_id>')
api.add_resource(ChannelResources, '/servers/<server_id>/channels')


@app.route('/oauth2/callback', methods=['GET'])
def callback():
    return jsonify({'status': 'success'})


if __name__ == '__main___':
    app.run(debug=True)
