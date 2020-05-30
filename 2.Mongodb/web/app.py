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
            'Sentence': "",
            'Tokens': 10
        })

        ret_json = {
            'status': 200,
            'message': 'You have succesfully connected to the API'
        }

        return ret_json, 200


class Store(Resource):
    def post(self):
        posted_data = request.get_json()
        username = posted_data['username']
        password = posted_data['password']
        sentence = posted_data['sentence']

        correct_pw = verify_pw(username, password)
        if not correct_pw:
            ret_json = {
                'status': 302,
                'message': 'Incorrect username or password'
            }
            return ret_json, 302

        num_tokens = count_tokens(username)
        if num_tokens <= 0:
            ret_json = {
                'status': 301,
                'message': 'Not enough tokens'

            }
            return ret_json, 301

        users.update({
            "Username": username},
            {"$set": {
                "Sentence": sentence,
                "Tokens": num_tokens - 1
            }
            }
        )

        ret_json = {
            'status': 200,
            'message': 'Sentence saved susccesfully'
        }

        return ret_json, 200


api.add_resource(Register, '/register')

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
