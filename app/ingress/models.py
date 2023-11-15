from pydantic import BaseModel, HttpUrl 


class IPs(BaseModel):
    ip: list[HttpUrl]


class Block(BaseModel):
    pow_token: str
    # block_content: str
    # predicessor: str
    # proposer_pk: str
    # nounce: str
