# import sys
# import pathlib
# import os

# sys.path.append((pathlib.Path(__file__).parent.parent).as_posix())

from app.utils.block_management import BlockData
from app.utils.ip_management import IpData
from app.utils.transaction_management import TransactionData


def main():
    BlockData().create_table()
    IpData().create_table()
    TransactionData().create_table()


if __name__ == '__main__':
    main()
