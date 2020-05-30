from flask import Flask, jsonify, request
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)


def check_posted_data(data, func_name):
    if func_name == 'add' or func_name == 'subtract' or func_name == 'multiply':
        if 'x' not in data or 'y' not in data:
            return 301
        else:
            return 200
    elif func_name == 'divide':
        if 'x' not in data or 'y' not in data:
            return 301
        elif data['y'] == 0:
            return 302
        else:
            return 200


class Add(Resource):
    def post(self):
        data = request.get_json()
        status_code = check_posted_data(data, 'add')
        if status_code != 200:
            ret = {
                "Message": "An error happened",
                "Status Code": status_code
            }
            return ret, status_code

        x = data['x']
        y = data['y']
        x = int(x)
        y = int(y)
        ret = x + y
        ret_map = {
            'Message': ret,
            'Status Code': status_code
        }
        return ret_map, 200


class Subtract(Resource):
    def post(self):
        data = request.get_json()
        status_code = check_posted_data(data, 'subtract')
        if status_code != 200:
            ret = {
                "Message": "An error happened",
                "Status Code": status_code
            }
            return ret, status_code

        x = data['x']
        y = data['y']
        x = int(x)
        y = int(y)
        ret = x - y
        ret_map = {
            'Message': ret,
            'Status Code': status_code
        }
        return ret_map, 200


class Multiply(Resource):
    def post(self):
        data = request.get_json()
        status_code = check_posted_data(data, 'multiply')
        if status_code != 200:
            ret = {
                "Message": "An error happened",
                "Status Code": status_code
            }
            return ret, status_code

        x = data['x']
        y = data['y']
        x = int(x)
        y = int(y)
        ret = x * y
        ret_map = {
            'Message': ret,
            'Status Code': status_code
        }
        return ret_map, 200


class Divide(Resource):
    def post(self):
        data = request.get_json()
        status_code = check_posted_data(data, 'divide')
        if status_code != 200:
            ret = {
                "Message": "An error happened",
                "Status Code": status_code
            }
            return ret, status_code

        x = data['x']
        y = data['y']
        x = int(x)
        y = int(y)
        ret = (x * 1.0) / y
        ret_map = {
            'Message': ret,
            'Status Code': status_code
        }
        return ret_map, 200


api.add_resource(Home, '/')
api.add_resource(Add, '/add')
api.add_resource(Subtract, '/subtract')
api.add_resource(Multiply, '/multiply')
api.add_resource(Divide, '/divide')

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
