import os

from agent import Agent
from messages import HumanMessage
from tools import tools


system_prompt = """
You run in a loop of Thought, Action, PAUSE, Observation.
At the end of the loop you output an Answer
Use Thought to describe your thoughts about the question you have been asked.
Use Action to run one of the actions available to you - then return PAUSE.
Observation will be the result of running those actions.

Your available actions are:

get_random_genre:
e.g. get_random_genre():
Returns a random genre


Example session:

Question: Hey, tell me a joke.
Thought: I should get a random genre and generate a joke based on that genre.
Action: get_random_genre()
PAUSE

You will be called again with this:

Observation: Comedy

You then output:

Answer: Here's a comedy joke for you!
"""


def _format_agent_reply(reply):
	if isinstance(reply, dict):
		return reply.get("content", str(reply))
	return getattr(reply, "content", str(reply))


def main():
	agent = Agent(system_prompt=system_prompt, tools=tools)

	print("Interactive chat started. Press Ctrl+C to exit.")
	while True:
		try:
			user_text = input("You: ").strip()
		except KeyboardInterrupt:
			print("\nBye!")
			break
		except EOFError:
			print("\nBye!")
			break

		if not user_text:
			continue

		reply = agent(HumanMessage(user_text))
		print(f"Assistant: {_format_agent_reply(reply)}")


if __name__ == "__main__":
	main()