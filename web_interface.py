from pyshop.pyshop import PyShop
from pyshop.pyshop import State
from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import behavior_gen
# import misty.misty_robot
import robot.social_robot as r


web = Flask(__name__)
CORS(web)

# @web.route('/behavior_generator', methods = ['POST'])
def start_robot():
    # robot = misty.misty_robot.Misty('192.168.1.4')
    robot = r.SocialRobot("127.0.0.1")    
    file = ['../Behavior_Gen/sarBehaviorGen/models/general.hddl']

    generator = behavior_gen.SarBehaviorGenerator(robot, file)
    # robot.startSkill()
    return generator

@web.route('/behavior_generator', methods = ['POST'])
def be_gen():
    generator = start_robot()
    data = json.loads(request.data)
    intent = data.get('Intent').get('name')
    affect = data.get('Affect')
    task = data.get('Task')
    verbal = data.get('Verbal')
    # print(intent)
    # print(affect)
    # print(task)
    # print(verbal)
    # print(data)

    state2 = State("test")
    state2.add(['rapport','low'])

    generator.performBehaviorFor([intent.lower()],state2)
    
    return jsonify(data)


if __name__ == '__main__':
   web.run(port=5000)


'''
To do list:
    Add more states (done)
    Get other levels of intent to work with preconditions 
    clean up code - good variable names :)  (done)
    new function to start engine - startskill + initiate robot  (done? I think it's calling start repeatedly still though)
'''