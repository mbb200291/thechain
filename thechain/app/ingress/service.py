import json

import sqlite3

from ..utils import block_management, ip_management, transaction_management


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


def sync_transaction_consensus():
    # with session:  # TODO: 
        for b in block_management.BlockData().iter_lonest_tx():
            # get transactions by giving b.transactions
            for tx in json.loads(b["content"]):
                if transaction_management.TransactionData().isin_tab(tx):
                    transaction_management.TransactionData().insert_tx(tx["content"])
                else:
                    transaction_management.TransactionData().undo_tx(tx["content"])
                    transaction_management.TransactionData().remove_tx(tx["content"])
    # session.commit() # TODO: 
