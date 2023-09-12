import aiofiles
import aiohttp
import ujson
from loguru import logger

from crawler.common.enums import ApiBaseUrl
from crawler.settings import AMAZON_LWA_CLIENT_ID, AMAZON_LWA_CLIENT_SECRET, REFRESH_TOKEN


class RestClient:
    def __init__(self, loop, token_type, access_token):
        self.loop = loop
        self.token_type = token_type.capitalize()
        self.access_token = access_token

    async def get(self, url: str, params: dict, profile_id: int):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"{self.token_type} "
                             f"{self.access_token}",
            'Amazon-Advertising-API-ClientId': AMAZON_LWA_CLIENT_ID,
            'Amazon-Advertising-API-Scope': str(profile_id)
        }
        session = aiohttp.ClientSession(
            loop=self.loop,
            headers=headers,
            json_serialize=ujson.dumps,
        )
        async with session.get(url, params=params) as response:
            logger.info(f'Response status: {response.status}')
            res = await response.json()
            logger.info(f'Response: {res}')

        await session.close()
        return res

    async def post(self, url: str, body, profile_id: int):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"{self.token_type} "
                             f"{self.access_token}",
            'Amazon-Advertising-API-ClientId': AMAZON_LWA_CLIENT_ID,
            'Amazon-Advertising-API-Scope': str(profile_id)
        }
        session = aiohttp.ClientSession(
            loop=self.loop,
            headers=headers,
            json_serialize=ujson.dumps,
        )
        async with session.post(url, json=body) as response:
            res = await response.json()
        await session.close()
        return res

    async def post_report(self, url: str, body, profile_id: int):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"{self.token_type} "
                             f"{self.access_token}",
            'Amazon-Advertising-API-ClientId': AMAZON_LWA_CLIENT_ID,
            'Amazon-Advertising-API-Scope': str(profile_id)
        }
        session = aiohttp.ClientSession(
            loop=self.loop,
            headers=headers,
            json_serialize=ujson.dumps,
        )
        async with session.post(url, json=body) as response:
            res = await response.read()
        await session.close()
        return ujson.loads(res.decode())

    async def get_report(self, profile_id: int, report_id: str):
        return await self.get(
            url=ApiBaseUrl.NORTH_AMERICA.value + f'/v2/reports/{report_id}',
            params={},
            profile_id=profile_id
        )

    async def download(self, profile_id: int, url: str, file) -> None:
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"{self.token_type} "
                             f"{self.access_token}",
            'Amazon-Advertising-API-ClientId': AMAZON_LWA_CLIENT_ID,
            'Amazon-Advertising-API-Scope': str(profile_id)
        }
        session = aiohttp.ClientSession(
            loop=self.loop,
            headers=headers,
            json_serialize=ujson.dumps,
        )
        f = await aiofiles.open(file, 'wb')
        async with session.get(url) as response:
            while True:
                chunk = await response.content.read(16144)
                if not chunk:
                    break
                await f.write(chunk)
            await f.close()
        await session.close()

    @staticmethod
    async def refresh_access_token(ref_tok):
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
        }
        body = {
            'grant_type': 'refresh_token',
            'client_id': AMAZON_LWA_CLIENT_ID,
            'client_secret': AMAZON_LWA_CLIENT_SECRET,
            'refresh_token': ref_tok
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(
                    url='https://api.amazon.com/auth/o2/token',
                    headers=headers,
                    data=body
            ) as response:
                res = await response.json()
        await session.close()
        return res
