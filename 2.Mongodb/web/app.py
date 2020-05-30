from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt

app = Flask(__name__)
api = Api(app)
# The client db name must match docker-compose db service
client = MongoClient("mongodb://db:27017")
db = client.sentencesDB
users = db['Users']

class Register(Resource):
    def post(self):
        posted_data = request.get_json()
        username = posted_data['username']
        password = posted_data['password']
        # Generate hash to securely store password
        hashed_pw = bcrypt.hashpw(password, bcrypt.gensalt())

        users.insert_many({
            'Username': username,
            'Password': hashed_pw,
            'Sentence': ""
        })

        ret_json = {
            'status': 200,
            'message': 'You have succesfully connected to the API'
        }

        return ret_json, 200


api.add_resource(Register, '/register')


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
