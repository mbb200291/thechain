import asyncio

from ..utils import block_management, transaction_management
from ..utils.custlog import setup_logger
from . import broadcasting
from ..config import GENESIS_BLOCK, PUBLIC_KEY 
from .service import create_valid_block


logger = setup_logger(__name__)


@broadcasting.broadcast_wrapper(1, "hangblock")
async def pack_block_attemp() -> dict[str, str]:
    result = await asyncio.to_thread(create_valid_block)
    return result


@broadcasting.broadcast_wrapper(300, "hangblocks")
def pack_local_known_blocks():
    return block_management.BlockData().dump_all_blocks()


@broadcasting.broadcast_wrapper(10, "testconn")
async def test_broadcast():
    print("run")
    return {"data": 1}
