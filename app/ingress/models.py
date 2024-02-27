# from pydantic import BaseModel, HttpUrl


# class IPs(BaseModel):
#     ip: list[HttpUrl]


# class Block(BaseModel):
#     pow_token: str  # sha256([md5(block_content, 128bits, 16bytes)] | md5(predicessor, 128bits, 16bytes) | md5(proposer_pk, 128, 16bytes)] | nounce (128, 16bytes)]) """
#     block_content: str
#     predicessor: str  # pow_token of predicessor
#     proposer_pk: str  # public key (PEM format) (base64 encoded)
#     nounce: str  # nounce bytes
