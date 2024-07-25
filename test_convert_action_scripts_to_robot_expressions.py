import converters.convert_action_scripts_to_robot_expressions as as_to_re

def test_breaking_up_single_expression():
    expressions = [
        {
            "name": "SayText",
            "args": ["hello"]
        },
        {
            "name": "SetEyes",
            "args": ["happy"]
        }
    ]
    
    broken_up_expressions = as_to_re.break_action_list_into_simultaneous_action_lists(expressions)

    assert len(broken_up_expressions) == 1

def test_breaking_up_two_expressions():
    expressions = [
        {
            "name": "SayText",
            "args": ["hello"]
        },
        {
            "name": "Pause",
            "args": ["1000"]
        },
        {
            "name": "SayText",
            "args": ["hello again"]
        },
    ]

    broken_up_expressions = as_to_re.break_action_list_into_simultaneous_action_lists(expressions)
    assert len(broken_up_expressions) == 2

def test_action_script_with_no_pauses():
    example_script = { 
  "intent": "Example", 
  "description": "This is an example of looking and speaking", 
  "actionList": [
{ 
"name": "LookInDirection", 
"args": ["center"] 
}, 
{ 
"name": "SetEyes", 
"args": ["happy"] 
}, 
{ 
"name": "SayText", 
"args": ["Hello, my name is Isabelle."] 
}]
}
    expression_list = as_to_re.convert_action_script_to_robot_expression(example_script)
    assert len(expression_list) == 1

    expression = expression_list[0]

    assert expression["speech"] == "Hello, my name is Isabelle."
    assert expression["title"] == "Hello, my name is Isabelle."
    assert expression["emotion"] == "happy"

def test_action_script_with_single_pause():
    example_script = { 
  "intent": "Example", 
  "description": "This is an example of looking and speaking", 
  "actionList": [
{ 
"name": "LookInDirection", 
"args": ["center"] 
}, 
{ 
"name": "SetEyes", 
"args": ["happy"] 
}, 
{ 
"name": "SayText", 
"args": ["Hello, my name is Isabelle."] 
}, 
{ 
"name": "Pause", 
"args": ["1500"] 
}, 
{ 
"name": "SetEyes", 
"args": ["default"] 
}, 
{ 
"name": "LookInDirection", 
"args": ["upperRight"] 
}] 
}

    expression_list = as_to_re.convert_action_script_to_robot_expression(example_script)
    assert len(expression_list) == 2

    first_expression = expression_list[0]

    assert first_expression["speech"] == "Hello, my name is Isabelle."
    assert first_expression["title"] == "Hello, my name is Isabelle."
    assert first_expression["emotion"] == "happy"
    
    second_expression = expression_list[1]

    assert second_expression["speech"] == ""
    assert second_expression["title"] == ""
    assert second_expression["emotion"] == "default"


if __name__ == "__main__":

    test_breaking_up_single_expression()
    test_breaking_up_two_expressions()
    test_action_script_with_no_pauses()
    test_action_script_with_single_pause()
