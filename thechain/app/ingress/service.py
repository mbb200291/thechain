import sqlite3

from ..utils import block_management, ip_management

# conn = sqlite3.connect('ip_database.sqlite')


def attemp_hangging(blocks):
    outcomes = []
    for block in blocks:
        if block_management.verify(block):
            outcomes.append(
                block_management.BlockData().hang_block(
                    block['pow_token'],
                    block['predicessor'],
                    block['transactions'],
                    block['proposer_pk'],
                    block['nounce'],
                    ))
        else:
            outcomes.append(0)
    return outcomes


def register_nodes(ips):
    ip_management.IpData().extend_ips(ips)
    return True


def unregister_nodes(ips):
    ip_management.IpData().remove_ips(ips)
    return True


def get_nodes():
    return ip_management.IpData().get_ips()
    

# def update_blocks(blocks):
#     return block_management.BlockData().update_blocks(blocks)
