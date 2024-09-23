import json
import argparse
import sys
import misty.misty_robot
import behavior_gen
from pyshop.pyshop import PyShop
from pyshop.pyshop import State

misty = misty.misty_robot.Misty("192.168.1.4.")
generator = behavior_gen.SarBehaviorGenerator(misty)

state = State(['affect', 'positive'])
gen_behavior = generator.performBehaviorFor(["social", "misty"], state)
