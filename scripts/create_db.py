import sys
import pathlib

sys.path.append(pathlib.Path(__file__).parent.parent.absolute().as_posix())

from app.ingress.modules.block_management import BlockData
from app.ingress.modules.ip_management import IpData


def main():
    BlockData().create_table()
    IpData().create_table()


if __name__ == '__main__':
    main()
    


