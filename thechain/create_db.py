# import sys
# import pathlib
# import os

# sys.path.append((pathlib.Path(__file__).parent.parent).as_posix())

from app.utils.block_management import BlockData
from app.utils.url_management import UrlData
from app.utils.transaction_management import TransactionData
# from app.utils.ledger_management import LedgerData


def main():
    BlockData().create_table()
    UrlData().create_table()
    TransactionData().create_table()
    TransactionData().bind_target_tabs([
        BlockData.TABNAME,
        UrlData.TABNAME,
        TransactionData.TABNAME,
    ])


if __name__ == '__main__':
    main()
