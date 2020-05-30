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


def verify_pw(username, password):
    hashed_pw = users.find({'Username': username})[0]['Password']
    if bcrypt.hashpw(password.encode('utf8'), hashed_pw) == hashed_pw:
        return True
    else:
        return False


def count_tokens(username):
    tokens = users.find({'Username': username})[0]['Tokens']
    return tokens


class Register(Resource):
    def post(self):
        posted_data = request.get_json()
        username = posted_data['username']
        password = posted_data['password']
        # Generate hash to securely store password
        hashed_pw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

        users.insert_one({
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
api.add_resource(Store, '/store')

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
