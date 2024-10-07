# import os
# import random
# import hashlib
# import dotenv
# import base64
import time

# from ..utils import db_managemenbt
from ..utils import block_management, transaction_management
# from ..utils.block_management import create_pow_token, create_nounce
from . import broadcasting
from ..config import GENESIS_BLOCK, PUBLIC_KEY 


@broadcasting.broadcast_wrapper(10, "hangblock")
def pack_block_attemp() -> dict[str, str]:
    round = 1
    while True:
        time.sleep(0.3)
        print("> round: %s" %round, end=' ')
        block = block_management.create_block()
        if block_management.verify_block_pow(block['pow_token']):
            print('[V]')
            return block
        else:
            print('[X]')
        round += 1


@broadcasting.broadcast_wrapper(10, "hangblocks")
def pack_local_known_blocks():
    return block_management.BlockData().get_all_blocks()


@broadcasting.broadcast_wrapper(10, "testconn")
def test_broadcast():
    print("run")
    return 1
