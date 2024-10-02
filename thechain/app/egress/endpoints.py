# import os
# import random
# import hashlib
# import dotenv
# import base64
import time

# from ..utils import db_managemenbt
from ..utils import block_management, transection_management
# from ..utils.block_management import create_pow_token, create_nounce
from . import broadcasting
from ..config import GENESIS_BLOCK, PUBLIC_KEY 


@broadcasting.broadcast_wrapper(10)
def pack_block_attemp() -> str:
    round = 1
    while True:
        time.sleep(0.3)
        print("> round: %s" %round)
        pow_token = block_management.create_pow_token(
            transection_management.TransactionData(
                ).get_unsync_transactions().encode('utf8'),
            block_management.base64decode(
                block_management.BlockData().get_tip()),
            PUBLIC_KEY,
            block_management.create_nounce()
            )
        if block_management.verify_block_pow(pow_token):
            return pow_token
        round += 1


@broadcasting.broadcast_wrapper(10)
def pack_local_known_blocks():
    block_management.BlockData().get_all_blocks()


async def router():
    await pack_block_attemp()
    await pack_local_known_blocks()
