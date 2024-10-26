from typing import Any, TypeAlias, TypedDict


GeneralDict: TypeAlias = dict[str, Any]


class MessageDictT(TypedDict):
    role: str
    content: str


class RequestDictT(TypedDict):
    model: str
    temperature: float
    messages: list[MessageDictT]
