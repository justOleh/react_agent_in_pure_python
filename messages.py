from dataclasses import dataclass


@dataclass
class Message:
    def __init__(self, role, content):
        self.role = role
        self.content = content

    def __repr__(self):
        return f"Message(role={self.role!r}, content={self.content!r})"


@dataclass
class SystemMessage(Message):
    def __init__(self, content):
        super().__init__(role="system", content=content)

    def __repr__(self):
        return f"SystemMessage(role={self.role!r}, content={self.content!r})"



@dataclass
class ToolResult(Message):
    def __init__(self, content):
        super().__init__(role="system", content=content)

    def __repr__(self):
        return f"ToolResult(role={self.role!r}, content={self.content!r})"


@dataclass
class AiMessage(Message):
    def __init__(self, llm_response):
        self.refusal = None
        self.annotations = None
        self.audio = None
        self.tool_calls = None
        self.raw = None

        self.parse_llm_response(llm_response)

    def __repr__(self):
        return (
            f"AiMessage(role={getattr(self, 'role', None)!r}, "
            f"content={getattr(self, 'content', None)!r}, "
            f"refusal={self.refusal!r}, annotations={self.annotations!r}, "
            f"audio={self.audio!r}, tool_calls={self.tool_calls!r}, raw={self.raw!r})"
        )

    def parse_llm_response(self, llm_response):
        pass


@dataclass
class HumanMessage(Message):
    def __init__(self, content):
        super().__init__(role="user", content=content)

    def __repr__(self):
        return f"HumanMessage(role={self.role!r}, content={self.content!r})"