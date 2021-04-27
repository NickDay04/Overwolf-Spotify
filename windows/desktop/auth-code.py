from werkzeug.wrappers import Request, Response
import json
from flask import Flask, request, jsonify
app = Flask(__name__)

with open ("jsonfile.json") as f:
    data = json.load(f)
    #data=f.read()

@app.route('/', methods=['GET', 'POST'])
def hello():
    return jsonify(data)

if __name__ == '__main__':
    from werkzeug.serving import run_simple
    run_simple('localhost', 9000, app)