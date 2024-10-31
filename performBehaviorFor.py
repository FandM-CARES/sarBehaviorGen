import json
import argparse
import sys
import misty.misty_robot
import behavior_gen
from pyshop.pyshop import PyShop
from pyshop.pyshop import State
import robot.social_robot as r

# misty = misty.misty_robot.Misty("192.168.1.4.")
robot = r.SocialRobot("127.0.0.1")    
file = ['/Users/vuhoanganh/Documents/BehaviorGen/sarBehaviorGen/models/misty.hddl']
generator = behavior_gen.SarBehaviorGenerator(robot, file)
# generator = behavior_gen.SarBehaviorGenerator(misty,['/Users/vuhoanganh/Documents/BehaviorGen/sarBehaviorGen/models/general.hddl'])
# misty.startSkill()

state = State("test")
state.add(['level','l4'])
state.add(['needsToBe', 'this piece', 'connect-corner', 'that piece'])

gen_behavior = generator.performBehaviorFor(["instruct"], state)
