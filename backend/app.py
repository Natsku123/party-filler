import logging
import os
from flask import Flask, jsonify, request
from flask_restful import reqparse, abort, Api, Resource
from flask_sqlalchemy import SQLAlchemy

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


class PartyResource(Resource):
    # TODO get party
    def get(self, party_id):
        return None
    def post(self):
        return None


class PartyResources(Resource):
    # TODO get parties
    def get(self):
        return None


class ServerResource(Resource):
    def get(self):
        return None
    def post(self):
        return None


class ServerResources(Resource):
    def get(self):
        return None


class ChannelResource(Resource):
    def get(self):
        return None
    def post(self):
        return None


class ChannelResources(Resource):
    def get(self):
        return None


api.add_resource(PartyResource, '/parties/<party_id>')
api.add_resource(PartyResources, '/parties')
api.add_resource(ServerResource, '/servers/<server_id>')
api.add_resource(ServerResources, '/servers')
api.add_resource(ChannelResources, '/servers/<server_id>/channels')


@app.route('/oauth2/callback', methods=['GET'])
def callback():
    logger.debug('OAUTH 2 CALLBACK: Full path: {0} Form: {1} JSON: {2}'.format(
        request.full_path,
        request.form,
        request.get_json
    ))
    return jsonify({'status': 'success'})


@app.route('/setup', methods=['POST'])
def setup():
    db.create_all()


if __name__ == '__main___':
    app.run(debug=True)
