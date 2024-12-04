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
   # sarBehaviorGen/models/misty.hddl
   file = ['models/misty.hddl']
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
      affectData = int(data.get('Affect'))
   if (affectData < 0):
      affect = "negative"
   elif (affectData > 0):
      affect = "positive"
   else:
      affect = "neutral"
    
   state = State("test")
   
   intent = data.get('Intent').get('name')
   if data.get('Intent').get('name') == 'instruct':
      needsToBe = []
      needsToBe.append('needsToBe')
      needsToBe.append(data.get('Intent').get('X'))
      if data.get('Intent').get('Y') != None:
         needsToBe.append(data.get('Intent').get('action'))
         needsToBe.append(data.get('Intent').get('Y'))
      else:
         needsToBe.append(data.get('Intent').get('action'))
         if data.get('Intent').get('loc') != None:
            needsToBe.append(data.get('Intent').get('loc'))
      state.add(needsToBe)
      print(needsToBe)
   if data.get('Intent').get('name') == 'followScript':
      script = []
      script.append('script')
      script.append('intro')
      script.append(data.get('Intent').get('script'))
      state.add(script)
   verbal = data.get('Verbal')
   rapport = data.get('Rapport')
   # next = str(data.get('Next')).split(" ")
   level = "l" + str(data.get('Level'))
   step = data.get('Step')
   taskState = data.get('Task')
   # script = data.get('Script').split(" ")

   state.add(['affect',affect])
   state.add(['taskState',taskState])
   state.add(['verbal',verbal])
   state.add(['rapport',rapport])
   state.add(['level',level])
   state.add(['step',step])
   
   generator.performBehaviorFor([intent],state)
    
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

    can we change reconcile belief in misty.hddl?
    
    rename "name" to intent,
    add more json objects to doaction's parameter
    changes on next move - less typing, guided buttons
    Followscript & reconcile belief
    demo - live demo -> video, what do in demo? :)

    When pressing button, record previous action -> recommend next action for script
    --> keep rotating & rotate little -> 1 option with scale for how much more they should rotate

   reconcile belief still has error.
   if it goes to i don't think so there might be additional preconditions.
   don't check the ones that requires only 1 piece but doesn't need location, it will not work.
      - flip, missing, remove
   
   misty.hddl script for simple actions like direction based on gaze of child
   all simple actions in misty.hddl cannot be called right now.
   
   https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.atatus.com%2Fblog%2Fpowerful-css-selectors%2F&psig=AOvVaw2LhKFtJf1faJrIzVDKt1sn&ust=1733259013117000&source=images&cd=vfe&opi=89978449&ved=0CBQQjRxqFwoTCIDM85L7iYoDFQAAAAAdAAAAABBR
    '''