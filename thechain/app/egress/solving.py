import os
import random
import hashlib
import dotenv
import base64

# from ..utils import db_managemenbt
from ..utils import block_management, transection_management
# from ..utils.block_management import create_pow_token, create_nounce
from .modules import broadcasting
from ..config import GENESIS_BLOCK, PUBLIC_KEY 


def pack_block_attemp() -> str:
    while True:
        pow_token = block_management.create_pow_token(
            transection_management.DbConnection(
                ).get_lastest_trans().encode('utf8'),
            block_management.base64decode(transection_management.DbConnection(
                ).get_tip()),
            PUBLIC_KEY,
            block_management.create_nounce()
            )
        if block_management.verify_block_pow(pow_token):
            return pow_token


# def main():
#     pow_token = pack_block_attemp()
    
    # dbm = block_management.DbConnection()
    # cur_target = base64.b64encode(GENESIS_BLOCK.decode('utf8'))
    # while True:
    #     temp = dbm.get_tip()
    #     if temp != cur_target:
    #         cur_target = temp
    #     powtoken = guess(cur_target)  # test create
    #     if block_management.verify_block_pow(powtoken):
    #         block_proposal = block_management.create_block(
    #             transaction,
    #             pred
    #         )
    #         broadcasting.broadcast(block_proposal)
    #         break
