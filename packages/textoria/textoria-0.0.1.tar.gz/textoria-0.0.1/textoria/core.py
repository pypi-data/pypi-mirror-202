from typing import Dict, Any
import aiohttp


class Textoria:
    def __init__(self, api_url: str):
        self.api_url = api_url

    async def get_all_keys(self) -> Dict[str, Any]:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.api_url}/get_all_keys") as response:
                response.raise_for_status()
                return await response.json()

    async def create_key(self, new_key: str, new_value: str) -> Dict[str, Any]:
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.api_url}/create_key",
                                    params={"new_key": new_key, "new_value": new_value}) as response:
                response.raise_for_status()
                return await response.json()

    async def update_key(self, key: str, new_value: str) -> Dict[str, Any]:
        async with aiohttp.ClientSession() as session:
            async with session.put(f"{self.api_url}/update_key",
                                   params={"key": key, "new_value": new_value}) as response:
                response.raise_for_status()
                return await response.json()

    async def delete_key(self, key: str) -> Dict[str, str]:
        async with aiohttp.ClientSession() as session:
            async with session.delete(f"{self.api_url}/delete_key",
                                      params={"key": key}) as response:
                response.raise_for_status()
                return await response.json()
