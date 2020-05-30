from flask import Flask, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bycript


app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.SimilarityDB
users = db["Users"]


def user_exists(username):
    if users.find({"Username": username}).count() == 0:
        return False
    else:
        return True


class Register(Resource):
    def post(self):
        posted_data = request.get_json()
        username = posted_data["username"]
        password = posted_data["password"]

        if user_exists(username):
            ret_json = {
                'status': 301,
                'message': "Invalid username"
            }
            return ret_json, 301

        hash_pw = bycript.hashpw(password.encode('utf8'), bycript.gensalt())

        users.insert_one({
            "Username": username,
            "Password": hash_pw,
            "Tokens": 6
        })

        ret_json = {
            'status': 200,
            'message': "You've successfully signed up to the API"
        }
        return ret_json, 200


