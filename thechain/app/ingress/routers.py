from fastapi import APIRouter, HTTPException

from .modules import ip_management, block_management
from .schemas import Block, HttpUrl


router = APIRouter()


@router.post('/register')
async def register(ips: list[HttpUrl]):
    ip_management.extend_ips(ips)
    return 1


@router.get('/operation-nodes')
async def get_operation_nodes() -> list[HttpUrl]:
    return ip_management.get_ips()


@router.post('/block')
async def post_block(block: Block):
    block = block.model_dump()
    if block_management.verify(block):
        result = block_management.hang_block(block)
        return {"status": result}
    else:
        return {"status": "in-correct"}
