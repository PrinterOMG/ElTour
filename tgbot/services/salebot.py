import aiohttp


class SalebotAPI:
    def __init__(self, api_key):
        self.api_key = api_key

    async def load_client(self, bot_username, telegram_id):
        url = f'https://chatter.salebot.pro/api/{self.api_key}/load_clients'
        payload = [
            {
                'platform_id': telegram_id,
                'group_id': bot_username,
                'client_type': 1
            }
        ]

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as response:
                if response.ok:
                    return await response.json(content_type='text/html')

    async def add_to_list(self, client_id, list_id):
        url = f'https://chatter.salebot.pro/api/{self.api_key}/add_to_list'
        payload = {
            'list_id': list_id,
            'clients': [client_id]
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as response:
                if response.ok:
                    return await response.json(content_type='text/html')

    async def remove_from_list(self, client_id, list_id):
        url = f'https://chatter.salebot.pro/api/{self.api_key}/remove_from_list'
        payload = {
            'list_id': list_id,
            'clients': [client_id]
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as response:
                if response.ok:
                    return await response.json(content_type='text/html')
