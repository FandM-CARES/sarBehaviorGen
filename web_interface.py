from pyshop.pyshop import PyShop
from pyshop.pyshop import State
from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import behavior_gen
import misty.misty_robot
import robot.social_robot as r

web = Flask(__name__)
CORS(web)
generator = None

@web.route('/start_robot', methods = ['POST'])
def start_robot():
    global generator
    robot = misty.misty_robot.Misty('192.168.1.4')
    robot.startSkill()
   #  robot = r.SocialRobot("127.0.0.1")    
    file = ['/home/zlocher/Documents/Computer Science Files/Research/Behavior_Gen/sarBehaviorGen/models/general.hddl']
    generator = behavior_gen.SarBehaviorGenerator(robot, file)
    if generator != None:
        return jsonify("Robot Started Successfully!")
    else:
       return jsonify("Robot Failed!")
    

@web.route('/behavior_generator', methods = ['POST'])
def be_gen():
    start_robot()
    if generator == None:
      return jsonify("Robot not Started")
    
    data = json.loads(request.data)

    affectData = int(data.get('Affect'))
    if (affectData < 0):
       affect = "negative"
    elif (affectData > 0):
       affect = "positive"
    else:
       affect = "neutral"
    
    taskState = data.get('Task')
    print(taskState)

    intent = data.get('Intent').get('name')
    level = "l" + str(data.get('Level'))
    verbal = data.get('Verbal')
    rapport = data.get('Rapport')
    next = data.get('Next')
    step = data.get('Step')

    state = State("test")
    state.add(['affect',affect])
    print(affect)
    state.add(['taskState',taskState])
    state.add(['verbal',verbal])
    state.add(['rapport',rapport])
    state.add(['next',next])
    state.add(['step',step])
    state.add(['level',level])

    generator.performBehaviorFor([intent.lower()],state)
    
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