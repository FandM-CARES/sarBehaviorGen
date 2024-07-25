"""File converts action scripts to robot expressions

Action scripts have the following attributes:
    intent: N/A
    description: N/A
    actionList: A list of Actions to consider

Each Action has two attributes name and args.

This converter only considers the following action names:
    "SayText", "SetEyes", "Pause"

"SayText" is used to determine the robot expression speech and title
"SetEyes" is used to determine the robot expression emotion (and TODO: color)
"Pause" is used to break up an action script into an order of asynchronous expressions
"""


def break_action_list_into_simultaneous_action_lists(action_list):
    """Split action list into expressions broken up by pauses

    Args:
        action_list (Action[]): A list of Actions

    Returns:
        Action[]: A list of Actions that would be expressed simultaneously
    """
    simultaneous_action_lists = []
    chunk = []
    for action in action_list:
        if action["name"] == "Pause":
            if len(chunk) > 0:
                simultaneous_action_lists.append(chunk)
            chunk = []
        else:
            chunk.append(action)

    if len(chunk) > 0:
        simultaneous_action_lists.append(chunk)

    return simultaneous_action_lists

def convert_simultaneous_action_list_to_expression(simultaneous_actions):
    """Convert a list of actions that would be performed simultaneously to a single robot expression

    Args:
        simultaneous_actions (Action[]): A list of actions that would be performed simultaneously

    Returns:
        Expression: A single robot expression summarizing the various forms of expression to perform
    """
    speech = ""
    title = ""
    color = "Light Blue"
    emotion = "Neutral"
    for action in simultaneous_actions:
        if action["name"] == "SayText":
            speech = action["args"][0]
            title = action["args"][0][:30]
        if action["name"] == "SetEyes":
            # TODO: Figure out both emotion and color from SetEyes
            emotion = action["args"][0]
            # color = action["args"][1]
    
    # TODO: Figure out what should happen if nothing was set (for example if simultaneous action list is only a gesture)
    return {
        "title": title,
        "speech": speech,
        "color": color,
        "emotion": emotion
    }

def convert_action_script_to_robot_expression(action_script):
    """Convert an action script to a list of synchrononous robot expressions

    Args:
        action_script (ActionScript): An action script describing a set of planned actions to perform

    Returns:
        Expression[]: A list of synchronous expressions as planned by the ActionScript
    """
    actions = action_script["actionList"]
    simultaneous_actions = break_action_list_into_simultaneous_action_lists(actions)
    return [convert_simultaneous_action_list_to_expression(simultaneous_action) for simultaneous_action in simultaneous_actions]
