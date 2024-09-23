from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import behavior_gen
import misty.misty_robot
from pyshop.pyshop import Pyshop, State


web = Flask(__name__)
CORS(web)

@web.route('/behavior_generator', methods = ['POST'])
def be_gen():
    data = json.loads(request.data)
    print(data)
    return jsonify(data)


if __name__ == '__main__':
   web.run(port=5000)