# from pydantic import BaseModel, HttpUrl


# class IPs(BaseModel):
#     ip: list[HttpUrl]


# class Block(BaseModel):
#     pow_token: str (b64 encoded)  # sha256([md5(transactions, 128bits, 16bytes)] | md5(predicessor, 128bits, 16bytes) | md5(proposer_pk, 128, 16bytes)] | nounce (128, 16bytes)]) """
#     transactions: str
#     predicessor: str  # pow_token of predicessor
#     proposer_pk: str  # public key (PEM format) (base64 encoded)
#     nounce: str  # nounce bytes (base64 encoded)
