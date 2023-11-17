from pydantic import BaseModel, HttpUrl 


class IPs(BaseModel):
    ip: list[HttpUrl]


class Block(BaseModel):
    
    pow_token: bytes  # [md5(block_content, 128bits)] | md5(predicessor, 128) | md5(proposer_pk, 128)] | nounce (128) """
    
    block_content: str
    predicessor: str  # pow_token of predicessor
    proposer_pk: str
    # nounce: str
