import logging
from flask import Flask, jsonify, request
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)

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


class Party(Resource):
    # TODO get party
    def get(self, party_id):
        return None
    def post(self):
        return None


class Parties(Resource):
    # TODO get parties
    def get(self):
        return None


class Server(Resource):
    def get(self):
        return None
    def post(self):
        return None


class Servers(Resource):
    def get(self):
        return None


class Channel(Resource):
    def get(self):
        return None
    def post(self):
        return None


api.add_resource(Party, '/parties/<party_id>')
api.add_resource(Parties, '/parties')
api.add_resource(Server, '/servers/<server_id>')
api.add_resource(Servers, '/servers')


@app.route('/oauth2/callback', methods=['GET'])
def callback():
    logger.debug('OAUTH 2 CALLBACK: Full path: {0} Form: {1} JSON: {2}'.format(
        request.full_path,
        request.form,
        request.get_json
    ))
    return jsonify({'status': 'success'})


if __name__ == '__main___':
    app.run(debug=True)
