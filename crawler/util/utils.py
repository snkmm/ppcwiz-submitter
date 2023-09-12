import aiohttp

from crawler.settings import AMAZON_LWA_CLIENT_ID, AMAZON_LWA_CLIENT_SECRET, REFRESH_TOKEN


async def refresh_access_token(ref_tok):
    url = 'https://api.amazon.com/auth/o2/token'
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
        async with session.post(url, headers=headers, data=body) as response:
            return await response.json()


async def fetch_profiles(access_token, token_type):
    url = 'https://advertising-api.amazon.com/v2/profiles'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'{token_type} {access_token}',
        'Amazon-Advertising-API-ClientId': AMAZON_LWA_CLIENT_ID
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            return await response.json()
