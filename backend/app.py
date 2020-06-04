from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)

# TODO more arguments as things are created
parser = reqparse.RequestParser()
parser.add_argument('party_id', type=int, help='ID of party')
parser.add_argument('discord_id', type=str, help='ID of discord user')
parser.add_argument('role_id', type=int, help='ID of role')
parser.add_argument('party', help="Party object")
parser.add_argument('player', help="Player object")


class Party(Resource):
    # TODO get party
    def get(self, party_id):
        return None


class Parties(Resource):
    # TODO get parties
    def get(self):
        return None


api.add_resource(Party, '/parties/<party_id>')
api.add_resource(Parties, '/parties')

if __name__ == '__main___':
    app.run(debug=True)
