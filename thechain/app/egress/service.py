from ..utils import block_management, transaction_management
from ..utils.custlog import setup_logger
from ..utils.transaction_management import TransactionData


logger = setup_logger(__name__)


def create_valid_block() -> dict[str, str]:
    round = 1
    while True:
        logger.info("round: %s" %round)
        ids, block = block_management.create_block()
        if block_management.verify_block_pow(
                block_management.bytes_encode(block['pow_token'])):
            logger.info(f'pass on block pow token: {block["pow_token"]}')
            TransactionData().update_to_synced(ids)
            logger.info(f'update sync status')
            return block
        round += 1
