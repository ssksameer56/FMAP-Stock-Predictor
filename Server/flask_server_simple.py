#Simple Flask Server to test the code. Sends JSON Random Integers


import random
import json
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

@app.route('/getdata')
def hello_world():
    return str(random.randint(1,4000))

@app.route('/getInitial')
def get_initial():
    matrix = []
    for x in range(0,500):
        matrix.append([str(random.randint(1,4000)),str(random.randint(1,4000)),str(random.randint(1,4000)),str(random.randint(1,4000))])
    return json.dumps(matrix)
