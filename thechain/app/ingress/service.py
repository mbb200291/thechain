import sqlite3

from .modules import ip_management, block_management

conn = sqlite3.connect('ip_database.sqlite')


def attemp_hangging(block):
    if block_management.verify(block):
        return block_management.hang_block(block)
    return None


def register_ip(ips):
    ip_management.extend_ips(ips)
    return True


def get_nodes():
    ip_management.get_ips()
    
    
def verify_message(prev_block, value) -> bool:
    return


def create_db():
    return
