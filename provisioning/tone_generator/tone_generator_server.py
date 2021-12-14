import os
from flask import Flask, request

app = Flask(__name__)

@app.route("/start")
def start():
    shape = request.args.get('shape') # this should be a number
    pitch = request.args.get('pitch') # this should also be a number
    # split this into process as per plans
    os.system(f'./utils/send-text.sh "{pitch},{shape}"')

@app.route("/stop")
def stop():
    os.system(f'./utils/send-text.sh "stop"')
