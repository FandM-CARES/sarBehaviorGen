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
   ip = json.loads(request.data)
   # robot = misty.misty_robot.Misty(ip)
   robot = r.SocialRobot("127.0.0.1")
       
   file = ['/Users/vuhoanganh/Documents/BehaviorGen/sarBehaviorGen/models/misty.hddl']
   generator = behavior_gen.SarBehaviorGenerator(robot, file)
   # robot.startSkill()
   
   if generator != None:
        return jsonify("Robot Started Successfully!")
   else:
       return jsonify("Robot Failed!")
    

@web.route('/behavior_generator', methods = ['POST'])
def be_gen():
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
   verbal = data.get('Verbal')
   rapport = data.get('Rapport')
   next = str(data.get('Next')).split(" ")
   level = "l" + str(data.get('Level'))
   step = data.get('Step')
   # script = data.get('Script').split(" ")

   state = State("test")
   state.add(['affect',affect])
   state.add(['taskState',taskState])
   state.add(['verbal',verbal])
   state.add(['rapport',rapport])
   state.add(['level',level])
   state.add(next)
   print(state)

   '''
   How to change the piece name and direction
   '''
   state.add(['step',step])

   # if intent == "Follow Script":
   #    intent == "followScript"
   #    if script == "intro":
   #       for i in range(1,6):
   #          state.add(['script',script + str(i+1)])
   #          generator.performBehaviorFor([intent.lower()],state)
   #          state.remove(['script',script + str(i+1)])
   #    elif script == "color":
   #       for i in range(6,12):
   #          state.add(['script',script + str(i)])
   #          generator.performBehaviorFor([intent.lower()],state)
   #          state.remove(['script',script + str(i)])
   #    elif script == "game":
   #       for i in range(12,19):
   #          state.add(['script',script + str(i)])
   #          generator.performBehaviorFor([intent.lower()],state)
   #          state.remove(['script',script + str(i)])
   #    return jsonify(data)
   
   generator.performBehaviorFor([intent.lower()],state)
    
   return jsonify(data)
   '''
   after the program finishes and return data to console, does the added state
   '''

if __name__ == '__main__':
   # web.run(host='192.168.1.5')
   web.run(port=5000)


'''
To do list:
    Add more states (done)
    Get other levels of intent to work with preconditions 
    clean up code - good variable names :)  (done)
    new function to start engine - startskill + initiate robot  (done? I think it's calling start repeatedly still though)

    Update UI - nextMove, step(stepName)

    can we change reconcile belief in misty.hddl?
    can we add everything from general.hddl to misty.hddl?
    
    rename "name" to intent,
    add more json objects to doaction's parameter
'''