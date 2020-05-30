from flask import Flask, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt
import spacy

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


def verify_pw(username, password):
    if not user_exists(username):
        return False

    hashed_pw = users.find({"Username": username})[0]["Password"]
    if bcrypt.hashpw(password.encode('uft8'), hashed_pw) == hashed_pw:
        return True
    else:
        return False


def count_tokens(username):
    tokens = users.find({"Username": username})[0]["Tokens"]
    return tokens


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

        hash_pw = bcrypt.hashpw(password.encode('utf8'), bycript.gensalt())

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


class Detect(Resource):
    def post(self):
        posted_data = request.get_json()
        username = posted_data["username"]
        password = posted_data["password"]
        text1 = posted_data["text1"]
        text2 = posted_data["text2"]

        if not user_exists(username):
            ret_json = {
                'status': 301,
                'message': "Invalid username"
            }
            return ret_json, 301

        correct_pw = verify_pw(username, password)
        if not correct_pw:
            ret_json = {
                'status': 302,
                'message': 'Invalid username or password'
            }

        num_tokens = count_tokens(username)
        if num_tokens <=0:
            ret_json = {
                'status': 303,
                'message': "out of tokens"
            }
            return num_tokens, 303

        nlp = spacy.load('en_core_web_sm')

        text1 = nlp(text1)
        text2 = nlp(text2)

        ratio = text1.similarity(text2)

        ret_json = {
            'status': 200,
            'similarity': "similarity score calculated"
            'score': ratio
        }

        current_tokens = count_tokens(username)
        users.update(
            {
                "Username": username,
                {
                    "$set": {"Tokens": current_tokens-1}
                }
            })

        return ret_json, 200


