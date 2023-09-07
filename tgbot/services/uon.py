import asyncio
from pprint import pprint

import aiohttp


class UonAPI:
    def __init__(self, api_key, _format='json'):
        self.api_key = api_key
        self._format = _format

    async def get_user_by_phone(self, phone):
        url = f'https://api.u-on.ru/{self.api_key}/user/phone/{phone}.{self._format}'

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 404:
                    return None

                result = await response.json()
                if result.get('users'):
                    return result['users'][0]
                return None

    async def create_user(self, name, phone, birthday=None):
        url = f'https://api.u-on.ru/{self.api_key}/user/create.{self._format}'
        payload = {
            'u_type': 1,
            'u_name': name,
            'u_phone_mobile': phone,
            'u_birthday': birthday
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as response:
                return await response.json()

    async def update_birthday(self, phone, birthday):
        user = await self.get_user_by_phone(phone)
        user_id = user.get('u_id')

        url = f'https://api.u-on.ru/{self.api_key}/user/update/{user_id}.{self._format}'
        payload = {
            'u_birthday': birthday
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as response:
                return await response.json()
