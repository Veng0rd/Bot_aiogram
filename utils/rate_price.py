import json
import aiohttp
from config_reader import config
from logger.logger import logger


@logger.catch
async def get_price() -> float | None:
    """ Возвращает цену доллара на данную минуту """
    parameters = {
        'slug': 'usd',
        'convert': 'RUB'
    }
    headers_settings = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': config.rate_price_token.get_secret_value()
    }
    async with aiohttp.ClientSession() as session:
        '''ClientSession создает сессию, тем самым сохраняет cookies и заголовки, работает эффективней'''
        session.headers.update(headers_settings)
        async with session.get(config.url_price, params=parameters) as response:
            price = await response.text()
            try:
                return float(str(json.loads(price)['data']['20317']['quote']['RUB']['price'])[:6])
            except KeyError:
                return None
