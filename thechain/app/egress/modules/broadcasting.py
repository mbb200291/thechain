import asyncio
import time

import aiohttp
import requests

from ...ingress.service import (
    get_nodes,
    )


async def send(url, session, block):
    try:
        async with session.post(url=url, data=block) as response:
            resp = await response.read()
            print("Successfully got url {} with resp of length {}.".format(url, len(resp)))
            return 1
    except Exception as e:
        print("Unable to get url {} due to {}.".format(url, e.__class__))
        return 0


async def broadcast(block):
    async with aiohttp.ClientSession() as session:
        rets = await asyncio.gather(
            *(send(url, session, block) for url in get_nodes()))
    return rets
