from flask import Flask, jsonify

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


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
