import logging
import os
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


class PartyResource(Resource):
    def get(self, party_id):
        return Party.query.filter_by(id=party_id).first()

    def post(self):
        server = parser.parse_args().get('server')
        if server is None:
            abort(400)
        return


class PartyResources(Resource):
    def get(self):
        return Party.query.order_by(Party.id.desc()).all()


class PartyPageResource(Resource):
    def get(self, page, per_page):
        return Party.query.order_by(Party.id.desc()).all().paginate(page, per_page)


class ServerResource(Resource):
    def get(self, server_id):
        return Server.query.filter_by(id=server_id).first()

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
api.add_resource(PartyPageResource, '/parties/page/<page>/per/<per_page>')
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
