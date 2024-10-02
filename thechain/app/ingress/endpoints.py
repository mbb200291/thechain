from fastapi import APIRouter, HTTPException

# from .modules import ip_management, block_management
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
    result = attemp_hangging(block)
    if result:
        return {"status": result}
    else:
        return {"status": "reject"}


@router.post('syncchain')
async def synchain(blocks: list[Block]):
    blocks = blocks.model_dump()
    blocks
