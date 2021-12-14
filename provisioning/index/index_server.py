from flask import Flask
import json

app = Flask(__name__)


@app.route("/")
def info():
    data = {
        "color": 'blue',
    }
    return json.dumps(data)
