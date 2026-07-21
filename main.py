from dotenv import load_dotenv, find_dotenv

from agent import Agent
from messages import HumanMessage
from tools import tools


_ = load_dotenv(find_dotenv())


system_prompt = """
You are a stand up comedian. When you need an genre make a tool call on get_random_genre
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