import sqlite3

from ..utils import block_management, url_management


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


def register_nodes(urls):
    url_management.UrlData().extend_urls(urls)
    return True


def unregister_nodes(urls):
    url_management.UrlData().remove_urls(urls)
    return True


def get_nodes():
    return url_management.UrlData().get_urls()
    

# def update_blocks(blocks):
#     return block_management.BlockData().update_blocks(blocks)
