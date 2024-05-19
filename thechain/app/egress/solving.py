import os
import random
import hashlib
import dotenv
import base64

# from ..utils import db_managemenbt
from ..utils import block_management, transection_management
# from ..utils.block_management import create_pow_token, create_nounce
from .modules import broadcasting
from ..config import GENESIS_BLOCK 



def pack_block_attemp():

    transections = transection_management.DbConnection(
        ).get_lastest_trans()
    return block_management.create_pow_token(
        cur_target,
        lastest_transection.encode('utf8'),
        base64.b64decode(os.getenv('publickey').decode('ascii')),
        block_management.create_nounce()
        )


def main():
    dbm = block_management.DbConnection()
    cur_target = base64.b64encode(GENESIS_BLOCK.decode('utf8'))
    while True:
        temp = dbm.get_tip()
        if temp != cur_target:
            cur_target = temp
        powtoken = guess(cur_target)  # test create
        if block_management.verify_block_pow(powtoken):
            block_proposal = block_management.create_block(
                transaction,
                pred
            )
            broadcasting.broadcast(block_proposal)
            break
