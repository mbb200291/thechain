import asyncio
import time
from functools import wraps

import aiohttp
# import requests

from ..utils.custlog import setup_logger
from ..ingress.service import (
    get_nodes,
    )

logger = setup_logger(__name__)

async def send(url, path, session, block):
    try:
        async with session.post(url=f'{url}/{path}', json=block) as response:
            resp = await response.read()
            logger.info("Successfully got url {} with resp of length {}.".format(url, len(resp)))
            return 1
    except Exception as e:
        logger.error(f"Unable to get url {url}", exc_info=True)
        return 0


async def broadcast(data, path):
    async with aiohttp.ClientSession() as session:
        rets = await asyncio.gather(
            *(send(url, path, session, data) for url in get_nodes()))
    return rets


def broadcast_wrapper(sec: int, path: str):
    def _broadcast_wrapper(func):
        @wraps(func)
        async def wrapped(*args, **kargs):
            while True:
                payload = await func(*args, **kargs)
                rets = await broadcast(payload, path)
                logger.info(rets)
                time.sleep(sec)
        return wrapped
    return _broadcast_wrapper
