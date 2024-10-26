from enum import StrEnum


class Model(StrEnum):
    GPT_35_TURBO = "gpt-3.5-turbo"


class Role(StrEnum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    FUNCTION = "function"


class Endpoint(StrEnum):
    CHAT_COMPLETION = "https://api.openai.com/v1/chat/completions"
