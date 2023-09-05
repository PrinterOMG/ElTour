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
                return await response.json()
