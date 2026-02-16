# Assitive Behavior Generator for Social Robots

This package provides an interface for generating and executing  assistive behaviors of social robots.  The behaviors are intended to communicate a given *intent* while also attempting to meet various social norms and conventions for turn-taking, rapport development, and supporting user autonomy.
While various social robot platforms having differing capabilities and available modalities, the design goal is to have the same behavior exhibited across multiple platforms.  The following is a demonstration video of a few behaviors that are run on the NAO and Mistry robots.

[![Watch a comparison of the NAO and Misty behaviors](https://img.youtube.com/vi/YDRcyy3Wsvc/0.jpg)](https://www.youtube.com/watch?v=YDRcyy3Wsvc)

The behavior generation uses an ontology of social behaviors, a planner, and middleware to communicate with the robots [\[2\]](#references).  The ontology, described further below, is realized in a hierarchical task network (HTN) model, and the planner (PyShop) uses this model to find a sequence of actions for the robot to perform.

The current HTN model can be found in models/misty.hddl.  This model describes behaviors for assisting a user on assembling a tangram puzzle.

The planner is PyShop, a derivative of Pyhop, both of which use the SHOP algorithm.  Unlike Pyhop, PyShop uses a declarative representation of the model, encoded in a hddl file.
You can download PyShop at https://github.com/FandM-CARES/pyshop.  You will need to install it to use the behavior generator.

This package also provides middleware to run the behaviors on social robots.  The goal is to provide a single definition of behaviors that may then be run on any social robot platform [2](#). Currently, there are two supported platforms: the NAO and Misty robots.
The Misty interface also requires a Skill running on the robot.  You can find the code for that Skill at https://github.com/FandM-CARES/psiMisty.
The NAO interfaces uses a local server to receive the behavior and then execute it on the robot.  That code can be found at
https://github.com/SturgeonInc/nao_api.

## Executing

You can begin to test the behavior generator once you have installed PyShop.
Then you can quickly test it by running the following command:
```
python3 behavior_gen.py
```
This will use the default robot interface, which simply prints each action in the behavior to the terminal.

### NAO

To test the interface to a NAO robot, try the following:
```
python3 behavior_gen.py --nao --address 192.168.1.3
```
Replace the IP address for the NAO robot.  The local server middleware is assumed to be running locally (127.0.0.1). 

### Misty

To test the interface to a Misty robot, try the following:
```
python3 behavior_gen.py --misty --address 192.168.1.3
```
Replace the IP address for the Misty robot. 

## Integration

Running this from the terminal is fun and all, but it will be more useful if you can integrate it into a larger system.  A key step in doing this is instantiating the `SarBehaviorGenerator`.  When creating the instance, you must provide a reference to a `robot`.  If you are interfacing with the NAO robot, that could would look something like this:
```
robot = nao.nao_robot.Nao(address)
```
See `behavior_gen.py` for further examples.

The primary function you need is `SarBehaviorGenerator.performBehaviorFor(intent, state)`, which will plan out the behavior and then execute it on the robot.


## Ontology for Modeling Behaviors

The `general.hddl` file describes a set of reusable behaviors.  This includes the more abstract *assistive intents* [\[1\](https://ojs.aaai.org/index.php/AAAI-SS/article/download/27674/27447), which are the basic types of communicative acts the robot may need to express.  The ontology from which these are derived describes the following types of intents:
- Task-oriented
	- Inform
	- Instruct
	- Confirm
	- Inquire (also Social)
	- Follow Script (also Social)
- Social
	- Persist

Basic turn-taking strategies are also included.  This includes a collectin of behavior for `take-turn` and `release-turn`.

A variety of other resuable behaviors are also provided.  This includes behaviors to wave, shake head, look around, and more.  

Finally, the file describes the basic actions that are available:
- SayText
- PointAt
- LookInDirection
- SetEyes (SetEmotion)
- TiltHead
- Pause

All of these actions are performed on the robot as non-blocking calls.  As a result, actions can be done nearly simultaneously by having them called one immediately after the other.  Currently, to have the next action be delayed and be performed after the previous one, the Pause action needs to be used. (Future developments will have options to allow each action to be synchronous or asynchronous).

In the models directory, other hddl files may be found that extend the general behaviors to provide assistance for a specific task.  For example, the `tangram.hddl` file is used to generate the necessary behaviors for supporting a child complete a tangram puzzle [\[1\](https://ojs.aaai.org/index.php/AAAI-SS/article/download/27674/27447).

## Robot Middleware

To perform the behaviors on the robot, each robot has middleware to support executing a list of actions on the robot.  Middleware for the Misty and NAO robots are currently supported.  Addtionally, the is a virtual robot for testing that only prints the actions to the terminal.

The middleware for each robot adheres to a [common API](https://github.com/FandM-CARES/sarBehaviorGen/docs/robot_middleware_API.pdf) that defines the list of supported actions and the required syntax.  By having a common API, the generated behaviors are similar across the different platforms \[2\].  

## References

\[1\] Yang, Y., Langer, A., Howard, L., Marshall, P. J., & Wilson, J. R. (2023). [Towards an Ontology for Generating Behaviors for Socially Assistive Robots Helping Young Children.](https://ojs.aaai.org/index.php/AAAI-SS/article/download/27674/27447) In *Proceedings of the AAAI Symposium Series* (Vol. 2, No. 1, pp. 213-218).

\[2\] Wilson, J. R. & Yang, Y. (2024). [Software Architecture to Generate Assistive Behaviors for Social Robots](https://fandm-cares.github.io/assets/pdf/wilsonyang2024software.pdf). In *HRI ’24 Companion*.