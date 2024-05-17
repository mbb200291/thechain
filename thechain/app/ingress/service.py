import sqlite3

from ..utils import block_management, ip_management

# conn = sqlite3.connect('ip_database.sqlite')


def attemp_hangging(block):
    if block_management.verify(block):
        return block_management.hang_block(block)
    return 0


def register_nodes(ips):
    ip_management.IpData().extend_ips(ips)
    return True


def unregister_nodes(ips):
    ip_management.IpData().remove_ips(ips)
    return True


def get_nodes():
    return ip_management.IpData().get_ips()
    

def hang_block(block):
    return block_management.BlockData().hang_block(
        block['pow_token'],
        block['predicessor'],
        block['block_content'],
        block['proposer_pk'],
        block['nounce'],
    )


# def verify_message(prev_block, value) -> bool:
#     return


# def create_db():
#     return
