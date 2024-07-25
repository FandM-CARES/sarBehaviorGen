from pyshop.pyshop import PyShop
from pyshop.pyshop import State
import json
import argparse
import sys

class SarBehaviorGenerator:

    def __init__(self, robot, filePaths=['models/general.hddl']):
        self.robot = robot
        self.init_planner(filePaths)
        self.last_plan = None

    def performBehaviorFor(self, intent, state):
        return self.performMultipleBehaviorsFor([intent], state)
        
    def performMultipleBehaviorsFor(self, intents, state):
        action_script = self.planBehaviorFor(intents, state)
        if action_script:
            robot.executeActionScript(action_script)
            return True
        else:
            print("No behavior found for " + str(intents))
            return False    
    
    def planBehaviorFor(self, intent, state):
        action_script = plan(state, intent, self.ps)
        if action_script:
            action_script = plan_converter(action_script)
            self.last_plan = action_script
            return action_script
        else:
            return False
        
    def trace_previous_action(self, action):
        if self.last_plan is not None:
            for step in self.last_plan:
                #if action['name'] == step[0][0]:
                if action['name'] == step['name']:
                    explanation = "The action " + action['name'] + " was performed,\n"
                    next_type = 'method'
                    #for trace in step[1:]:
                    for trace in step['metadata']['trace']:
                        if next_type == 'method':
                            explanation += "which was part of the method " + trace[0] + ",\n"
                            next_type = 'task'
                        elif next_type == 'task':
                            explanation += "for the task " + trace[0] + "\n"
                            next_type = 'method'
                    return explanation

    def init_planner(self, filePaths):
        self.ps = PyShop('init')

        for fp in filePaths:
            self.ps.declare_methods(fp)   
            self.ps.declare_operators(fp)  
        
        # ps.print_operators()
        # ps.print_methods()


def create_state():
    return State("1")


def plan(state, task, ps):
    return ps.pyshop(state, task, 3)
    

def plan_converter(plan):

    if plan == False:
        return False # if there is no plan


    dictionary_list = []
    for line in plan:
    
        dict = {}
        action = line[0]
        key = action[0]
        val = action[1:]
        dict['name'] = key
        dict['args'] = val

        dictionary_list.append(dict)

        json_obj = json.dumps(dictionary_list)
    return dictionary_list


#################
# Test Scenarios
#################

def scenario1(state1,ps):
    #Scenario-1 offer-help-question
    state1.add(["confusion", "early"])
    state1.add(["level", "l2"])
    return state1, ["inquire", "misty"]
    #return plan(state1, [["inquire", "misty"]], ps)

def scenario2(state1,ps): #test persist doing-great
    state1.add(["time", "long"])
    state1.add(["level","l2"])
    state1.add(["game", "no-error"])
    return state1, ["persist", "misty"]
    # return plan(state1, [["persist", "misty"]], ps)

def scenario3(state1, ps): #test correct not-touching
    state1.add(["game", "not-touching"])
    return state1, ["correct", "misty"]
    # return plan(state1, [["correct", "misty"]], ps)

def scenario4(state1, ps): #test instruct level 3 missing
    state1.add(["needsToBe", "blue small triangle", "missing", "found"])
    state1.add(["level","l3"])
    return state1, ["instruct", "misty"]
    # return plan(state1, [["instruct", "misty"]],ps)

def scenario5(state1, ps): #test instruct level 4
    state1.add(["needsToBe","small blue triangle", "spin", "right"])
    state1.add(["level", "l4"])
    return state1, ["instruct", "misty"]
    # return plan(state1, [["instruct", "Misty"]], ps)

def scenario6(state1, ps): #test intro 
    state1.add(["intro", "2"])
    return state1, ["greeting", "misty"]
    # return plan(state1, [["greeting", "Misty"]], ps)

def scenario7(state1, ps): #test confirm
    #state1.add(["interaction", "short"])
    state1.add(["level", "l1"])
    return state1, ["confirm", "misty"]
    # return plan(state1, [["confirm", "misty"]], ps)

def scenario8(state1, ps): #test instruct level 3
    state1.add(["needsToBe","small blue triangle", "spin", "left"])
    state1.add(["level", "l4"])
    return state1, ["instruct", "misty"]
    # return plan(state1, [["instruct", "Misty"]], ps)

def scenario9(state1, ps): #test instruct level 3
    state1.add(["level", "l2"])
    return state1, ["missingPiece", "misty"]
    # return plan(state1, [["missingPiece", "Misty"]], ps)


def scenario10(state1, ps): #test instruct swap
    state1.add(["needsToBe", "red medium triangle", "swap", "large orange triangle"])
    state1.add(["level", "l4"])
    return state1, ["instruct", "misty"]
    # return plan(state1, [["instruct", "Misty"]], ps)

def scenario11(state1, ps): #test instruct move
    state1.add(["needsToBe", "red medium triangle", "move", "lowerRight"])
    state1.add(["level", "l4"])
    return state1, ["instruct", "misty"]
    # return plan(state1, [["instruct", "Misty"]], ps)


def scenario12(state1, ps): #test release turn 
    state1.add(["gaze", "away"])
    state1.add(["affect", "negative"])
    return state1, ["task-turn", "misty"]
    # return plan(state1, [["take-turn", "misty"]], ps)

def scenario13(state1, ps): #test relase turn
    state1.add(["gaze", "away"])
    state1.add(["affect", "negative"])
    return state1, ["release-turn", "misty"]
    # return plan(state1, [["release-turn", "misty"]], ps)

def scenario14(state1, ps):
    state1.add(["level","l1"])

def run_test(function, beh_gen):

    state1 = create_state()
    state1, intent = function(state1, None)
    try:
        if beh_gen.performBehaviorFor(intent, state1):
            print("Action executed!\nTest Complete")
        else:
            print("Execution Failed :(")
    except:
        print("Execution Error :(")

if __name__ == '__main__':

    #runTest()
    parser = argparse.ArgumentParser()
    parser.add_argument('test', default='test1', nargs='?')
    parser.add_argument('--file', default=['models/general.hddl'], action='append')
    parser.add_argument('--address', default='192.168.1.3')
    parser.add_argument('--interactive', action='store_true')
    parser.add_argument('--nao', action='store_true')
    parser.add_argument('--misty', action='store_true')
    args = parser.parse_args()
    
    
    if args.nao:
        import nao.nao_robot
        robot = nao.nao_robot.Nao(args.address)
    elif args.misty:
        import misty.misty_robot
        robot = misty.misty_robot.Misty(args.address)
    else:
        import robot.social_robot as r
        robot = r.SocialRobot(args.address)
        
    robot.startSkill()
    args.file.reverse() # ensures the default behaviors are last/deprioritized
    beh_gen = SarBehaviorGenerator(robot, args.file)

    if args.interactive:
        state1 = State("interactive")
        state1.add(["level", "l4"])
        state1.add(["taskState","unstarted"])
        state1.add(["gaze","task"])
        state1.add(["rapport","medium"])
        state1.add(["affect","neutral"])
        state1.add(["needsToBe", "small blue triangle", "slide", "right"])
        state1.add(["intro","8"])
        state1.add(["verbal", "hello"])

        last_plan = ''
        user_input = '?'
        while user_input[0] != 'q':
            user_input = input('Enter command ([a]dd, [r]emove, [l]ist, [p]lan intent args, [t]race action, [q]uit):')

            if len(user_input) == 0:
                user_input = last_plan

            if (user_input[0] == "a"):
                #add_fact = input ('add a fact in the format of [level, l2]: ')
                add_fact= user_input[2:]
                add_fact = add_fact.strip('][').split(', ')
                for fact in state1.facts:
                    if (fact[0] == add_fact[0]):
                        state1.remove(fact)
                state1.add(add_fact)

            if (user_input[0] == "r"):
                #rm_fact = input('Enter the number of the fact to remove:')
                rm_fact = user_input[2:]
                for fact in state1.facts:
                    if (fact[0] == rm_fact[0]):
                        state1.remove(fact)

            if (user_input[0] == "l"):
                print(state1.facts)

            if (user_input[0] == "p"):
                #task = input ('Enter task in the format [instruct, misty]: ')
                last_plan = user_input
                if len(user_input) < 2:
                    print("Enter intent and args (e.g., p instruct misty)")
                else:
                    task = user_input[2:]
                    task = task.split(' ')

                    beh_gen.performBehaviorFor(task, state1)

            if (user_input[0] == "t"):
                action = user_input[2:]
                print(beh_gen.trace_previous_action({'name':action}))
            # if user_input[0] == 'q':
            #     break
        

    else:
        test_id = args.test[4]
        func = vars()["scenario"+str(test_id)]
        run_test(func, beh_gen)




