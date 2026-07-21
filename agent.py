import json

from openai import OpenAI

from messages import Message, SystemMessage, ToolResult


class Agent:
    def __init__(self, system_prompt="", tools=None):
        self.__memory = self.__init_memory()
        self.__model_type = "gpt-5-nano"
        self.__client = OpenAI()
        self.__tool_registry = self.__register_tools(tools or [])

        self.__system_prompt = system_prompt
        self.__save_message(SystemMessage(system_prompt))

    def __register_tools(self, tools):
        tool_registry = {tool.get_function_name(): tool for tool in tools}
        return tool_registry

    def __call__(self, user_message):
        self.__execute(user_message)
        return self.__get_last_message()

    def __invoke_client(self, messages):
        chat_completion = self.__client.chat.completions.create(
            model=self.__model_type,
            messages=messages,
            tools=[tool.to_dict() for tool in self.__tool_registry.values()]
        )
        return chat_completion

    def __init_memory(self):
        return []

    def __save_message(self, message):
        self.__memory.append(message)

    def __parse_tool_call(self, call):

        raw_args = call.function.arguments or "{}"

        tool_call = {
            "tool_call_id": call.id,
            "tool_name": call.function.name,
            "raw_args": raw_args,
            "args": json.loads(raw_args)
        }
        return tool_call

    def __extract_messages_from_memory(self):
        messages = []
        for message in self.__memory:
            if isinstance(message, dict):
                messages.append(message)
                continue

            if isinstance(message, ToolResult):
                payload = json.loads(message.content)
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": payload["tool_call_id"],
                        "content": json.dumps(payload["result"]),
                    }
                )
                continue

            messages.append({"role": message.role, "content": message.content})
        return messages

    def __get_last_message(self):
        return self.__memory[-1]

    def __call_tool(self, parsed_call):
        tool_name = parsed_call["tool_name"]
        tool = self.__tool_registry.get(tool_name)
        if tool is None:
            return {"error": f"Tool not found: {tool_name}"}

        args = parsed_call.get("args") or {}
        return tool(**args)

    def __execute(self, message: Message):
        self.__save_message(message)

        max_iterations = 8
        for _ in range(max_iterations):
            messages = self.__extract_messages_from_memory()
            llm_response = self.__invoke_client(messages)

            choice = llm_response.choices[0]
            ai_message = choice.message
            ai_content = ai_message.content or ""

            if ai_message.tool_calls:
                assistant_with_tools = {
                    "role": "assistant",
                    "content": ai_content,
                    "tool_calls": [
                        {
                            "id": call.id,
                            "type": "function",
                            "function": {
                                "name": call.function.name,
                                "arguments": call.function.arguments or "{}",
                            },
                        }
                        for call in ai_message.tool_calls
                    ],
                }
                self.__save_message(assistant_with_tools)
            else:
                self.__save_message(Message(role="assistant", content=ai_content))

            if "end_turn" in ai_content:
                break

            if not ai_message.tool_calls:
                break

            for call in ai_message.tool_calls:
                parsed_call = self.__parse_tool_call(call)
                tool_output = self.__call_tool(parsed_call)

                tool_result = ToolResult(
                    content=json.dumps(
                        {
                            "tool_call_id": parsed_call["tool_call_id"],
                            "tool_name": parsed_call["tool_name"],
                            "result": tool_output,
                        }
                    )
                )
                self.__save_message(tool_result)


        return self.__get_last_message()