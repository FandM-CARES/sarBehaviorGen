from pyshop.pyshop import PyShop
from pyshop.pyshop import State
from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import behavior_gen
import misty.misty_robot


web = Flask(__name__)
CORS(web)

@web.route('/behavior_generator', methods = ['POST'])
def be_gen():
    robot = misty.misty_robot.Misty('192.168.1.4')
    file = ['models/general.hddl']
    generator = behavior_gen.SarBehaviorGenerator(robot, file)

    data = json.loads(request.data)
    Payload = data.get('Payload')
    intent = Payload.get('name')
    # affect = affect.get('name')
    print(data)

    state2 = State("test")
    state2.add(['rapport','low'])

    robot.startSkill()
    generator.performBehaviorFor([intent.lower()],state2)
    
    return jsonify(data)


if __name__ == '__main__':
   web.run(port=5000)


'''
To do list:
    Add more states
    Get other levels of intent to work with preconditions
    clean up code - good variable names :)
    new function to start engine - startskill + initiate robot
'''