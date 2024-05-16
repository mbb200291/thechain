import os
import random
import hashlib
import dotenv
import base64

# from ..utils import db_management
from ..ingress.modules import block_management
from .modules import broadcasting, transections_management


def create_nounce():
    rand = random.randint(0, 128)
    return bytes(rand)


def cal_md5(content: bytes):
    hasher = hashlib.md5()
    hasher.update(content)
    return hasher.digest()


def create_pow_token(prev: str, transection: str, privatekey: str,
                     nounce: bytes = bytes(4)):
    hasher = hashlib.sha256()
    hasher.update(cal_md5(transection.encode('utf8')))
    hasher.update(cal_md5(prev.encode('utf8')))
    hasher.update(base64.b64decode(privatekey))
    hasher.update(nounce)
    return hasher.digest()


def guess(cur_target):
    lastest_transection = transections_management.DbConnection(
        ).get_lastest_trans()
    return create_pow_token(
        cur_target,
        lastest_transection,
        os.getenv('privatekey'),
        create_nounce()
        )


def main():
    dbm = block_management.DbConnection()
    cur_target = 'thegenesisblock'
    while True:
        temp = dbm.get_tip()
        if temp != cur_target:
            cur_target = temp
        attempoutcome = guess(cur_target)
        if block_management.verify_block_pow(attempoutcome):
            broadcasting.broadcast()
            break
