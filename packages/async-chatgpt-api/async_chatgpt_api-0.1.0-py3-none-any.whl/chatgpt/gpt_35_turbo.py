from chatgpt.enums import Endpoint, Model, Role
from chatgpt.errors import ChatGPTGeneralError
from .types import RequestDictT
from .basic_model import BaseModel


class GPT35_Turbo(BaseModel):
    def __init__(self, api_key: str, temperature: float = 1.0) -> None:
        super().__init__(
            api_key,
            Model.GPT_35_TURBO,
            Endpoint.CHAT_COMPLETION,
            temperature=temperature,
        )

    async def system_prompt(self, prompt: str) -> str:
        data: RequestDictT = {
            "model": self.model,
            "temperature": self.temperature,
            "messages": [
                {"role": Role.SYSTEM, "content": prompt},
            ],
        }

        resp = await self._request(data)
        if resp.get("error", False):
            raise ChatGPTGeneralError(f"Open AI ChatGPT API says: {resp}")
        return str(resp["choices"][0]["message"]["content"])
