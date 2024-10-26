import json
import aiohttp

from .types import GeneralDict, RequestDictT


class BaseModel:
    def __init__(
        self, api_key: str, model: str, base_endpoint: str, temperature: float = 1.0
    ) -> None:
        self.api_key = api_key
        self.model = model
        self.temperature = temperature
        self._completions_endpoint = base_endpoint
        self._aiohtt_client = aiohttp.ClientSession()

    def get_headers(self) -> GeneralDict:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        return headers

    async def close(self) -> None:
        if not self._aiohtt_client.closed:
            await self._aiohtt_client.close()

    async def _request(
        self, data: GeneralDict | RequestDictT, method: str = "POST"
    ) -> GeneralDict:
        async with self._aiohtt_client.request(
            method=method,
            url=self._completions_endpoint,
            headers=self.get_headers(),
            data=json.dumps(data),
        ) as resp:
            await resp.read()

        return dict(await resp.json())
