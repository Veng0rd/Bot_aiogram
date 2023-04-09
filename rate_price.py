import json
import aiohttp
from config_reader import config


async def get_price():
    parameters = {
        'slug': 'usd',
        'convert': 'RUB'
    }
    headers_settings = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': config.rate_price_token.get_secret_value()
    }
    async with aiohttp.ClientSession() as session:
        session.headers.update(headers_settings)
        async with session.get(config.url_price, params=parameters) as response:
            price = await response.text()
            return str(json.loads(price)['data']['20317']['quote']['RUB']['price'])[:6]
