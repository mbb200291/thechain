from ..utils import block_management, transaction_management
from ..utils.custlog import setup_logger
# from ..config import GENESIS_BLOCK, PUBLIC_KEY 


logger = setup_logger(__name__)


def create_valid_block() -> dict[str, str]:
    round = 1
    while True:
        logger.info("round: %s" %round)
        block = block_management.create_block()
        if block_management.verify_block_pow(
                block_management.bytes_encode(block['pow_token'])):
            logger.info(f'pass on block pow token: {block['pow_token']}')
            return block
        round += 1
