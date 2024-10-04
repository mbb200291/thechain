from fastapi import APIRouter, HTTPException
from typing import Optional

from ..utils import block_management
from .schemas import Block, HttpUrl
from .service import (attemp_hangging, register_nodes, get_nodes,
                      unregister_nodes)

router = APIRouter()


@router.post('/register')
async def register(ips: list[HttpUrl]):
    register_nodes(ips)
    return 1


@router.delete('/unregister')
async def unregister(ips: list[HttpUrl]):
    unregister_nodes(ips)
    return 1


@router.get('/nodes')
async def get_operation_nodes() -> list[HttpUrl]:
    return get_nodes()


@router.post('/hangblock')
async def hang_block(block: Block):
    block = block.model_dump()
    result = attemp_hangging([block])
    if result[0]:
        return {"status": 1}
    else:
        return {"status": "reject"}


@router.post('/syncchain')
async def synchain(blocks: list[Block]):
    blocks = blocks.model_dump()
    return attemp_hangging(blocks)


@router.get('/blocks')
async def get_blocks() -> list[Block]:
    blocks = block_management.BlockData().dump_all_blocks()
    return blocks


@router.post('/block/testcreate')
async def create_block(predicessor: Optional[str] = None,
                       transactions: Optional[str] = None) -> Block:
    block = block_management.create_block(predicessor, transactions)
    return block
