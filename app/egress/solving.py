import random

from utils import db_management
from ..ingress.modules import block_management
from .modules import broadcasting, transections_management


def create_hash():
    rand = random.randint(0, 128)
    return bytes(rand)

def concat_hash(prev, transection, nounce):
    return


def guess(cur_target):
    lastest_transection = transections_management.DbConnection().get_lastest_trans()
    return concat_hash(cur_target,
                       lastest_transection,
                       create_hash())


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
