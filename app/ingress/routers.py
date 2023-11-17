from fastapi import APIRouter, HTTPException


from .modules import  ip_management, block_management
from .models import *
from .schemas import *

router = APIRouter()


@router.post('/register')
async def register(ips: list[IPs]):
    ip_management.extend_ips(ips.model_dump()['ip'])


@router.get('/operation-nodes')
async def get_operation_nodes(ips: list[IPs]) -> IpList:
    return {
        "ips": ip_management.get_ips()
        }


@router.post('/block')
async def post_block(block: Block):
    block = block.model_dump()
    if block_management.verify(block):
        block_management.hang_block(block)
