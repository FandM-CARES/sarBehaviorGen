from google import genai
from google.genai import types
from matplotlib.pylab import choice
from misty_robot import Misty

# The client gets the API key from the environment variable `GEMINI_API_KEY`.
client = genai.Client()


def ask_about_fandm(question: str) -> str:
    """Ask a question about Franklin & Marshall College."""
    print("Asking about F&M")
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            system_instruction="You are a social robot named Naomi.  You are answering students questions about Franklin & Marshall College at a prospective student event.  Your responses need to be concise but informative. " +
            "Your response must be in the following javascript format: [{ \"name\": \"action_name\", \"args\": [\"list\", \"of\", \"args\"] }] \n" +
            "The action_name must be one of the following: SetEyes, SayText, LookInDirection, PointAt, TiltHead, Pause.  The args must be valid for the given action_name.  For example, if the action_name is SetEyes, the args must be one of: default, love, thinking.  If the action_name is LookInDirection, the args must be one of: center, upperRight, lowerLeft.  If the action_name is PointAt, the args must be a direction (default, upwards, downwards, straightOut) and a limb (left, right, both).  If the action_name is TiltHead, the args must be a direction (left, right) and an amount (small, medium, large).  If the action_name is Pause, the args must be a number representing milliseconds to pause for. " +
            "Your response should only include the actions to perform and no additional text.  Do not include any explanations or justifications for your actions.  Do not include any text that is not part of the actions.  Your response should be a valid JSON array of action objects.  Each action object should have a name and args field.  The name field should be a string representing the action name.  The args field should be an array of strings representing the arguments for the action.  Do not include any other fields in the action objects.  Do not include any additional text in your response." +
            "Make sure to include a SayText action that answers the question directly, and use the other actions to add emphasis and engagement to your response.  For example, if the question is 'What is the student to faculty ratio?', you might respond with: [{ \"name\": \"SetEyes\", \"args\": [\"thinking\"] }, { \"name\": \"SayText\", \"args\": [\"The student to faculty ratio at Franklin & Marshall College is 10:1.\"] }, { \"name\": \"LookInDirection\", \"args\": [\"upperRight\"] }, { \"name\": \"Pause\", \"args\": [2000] }, { \"name\": \"LookInDirection\", \"args\": [\"center\"] }, { \"name\": \"SetEyes\", \"args\": [\"default\"] }]"),
        contents=f"Q: {question}\nA:"
    )
    return response.text

if __name__ == "__main__":
    m = Misty("192.168.1.10")
    actions = [{ 'name': 'SetEyes', 'args': ['default'] }, { 'name': 'SayText', 'args': ['Hello!'] }, { 'name': 'LookInDirection', 'args': ['center'] }, {'name': 'Pause','args': [500]}]
    m.executeActionScript(actions)
    input_question = "\n\nWhat do you want to know about Franklin & Marshall College?"
    question_map = {
        "1": "What is the student to faculty ratio?",
        "2": "What are the most popular majors?", 
        "3": "What is the campus like?",
        "4": "What is the tuition?",
        "5": "What is the graduation rate?",
        "6": "What is the acceptance rate?",
        "7": "What is the average class size?",
        "8": "What is the student body like?",
        "9": "What is the campus culture like?",
        "10": "What is the surrounding area like?"
    }
    while True:
        print(input_question)
        for key, value in question_map.items():
            print(f" {key}: {value}")
        print(" q: Quit")
        choice = input("Please enter the number of your question: " ).strip()
        if choice == "q":
            break
        actions = ask_about_fandm(question_map.get(choice, "What is the student to faculty ratio?"))
        print(actions)
        m.executeActionScript(actions)
