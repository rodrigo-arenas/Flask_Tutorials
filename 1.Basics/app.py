from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/')
def hello_world():
    return "hello world!"


@app.route('/info')
def information():
    return jsonify({
        "Name": "FlaskApp",
        "Version": 0.1
    })


@app.route("/add_two_nums", methods=["POST"])
def add_tow_nums():
    data = request.get_json()
    x = data['x']
    y = data['y']
    z = x+y
    return jsonify(z)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
