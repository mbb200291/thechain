import asyncio
import time

import aiohttp
# import requests

from ..ingress.service import (
    get_nodes,
    )


async def send(url, path, session, block):
    try:
        async with session.post(url=f'{url}/{path}', data=block) as response:
            resp = await response.read()
            print("Successfully got url {} with resp of length {}.".format(url, len(resp)))
            return 1
    except Exception as e:
        print("Unable to get url {} due to {}.".format(url, e.__class__))
        return 0


async def broadcast(data, path):
    async with aiohttp.ClientSession() as session:
        rets = await asyncio.gather(
            *(send(url, path, session, data) for url in get_nodes()))
    return rets


def broadcast_wrapper(sec: int, path: str):
    def _broadcast_wrapper(func):
        def wrapped():
            while True:
                time.sleep(sec)
                payload = func()
                rets = broadcast(payload, path)
                print(rets)
        return wrapped
    return _broadcast_wrapper
