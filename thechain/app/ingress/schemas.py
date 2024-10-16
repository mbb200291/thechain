import os

from pydantic import BaseModel, HttpUrl

# from config import GENESIS_BLOCK

# class UrlList(BaseModel):
#     urls: list[str]

class Transaction(BaseModel):
    content: str
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "content": "SELECT * FROM Ledger"
                }
            ]
        }
    }

class Block(BaseModel):
    pow_token: str  # base64 encoded of sha256([md5(transactions, 128bits, 16bytes)] | predicessor pow_token, 256bits, 32bytes) | proposer_pk (depends on algorithm)) | nounce (128, 16bytes)]) """
    transactions: str  # transaction string encoded in UTF8 (and base64 further encode as string)
    predicessor: str  # pow_token of predicessor (base encoded string)
    proposer_pk: str  # public key (PEM format) (base64 encoded string)
    nounce: str  # nounce bytes (base64 encoded string)
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "pow_token": "7a82hNISXLNsANBp1NsJSLy5vSUJcW4Cy7yA/KmW5iQ",
                    "predicessor": "thegenesisblock=",
                    "transactions": "test input",
                    "proposer_pk": os.getenv("PUBLIC_KEY"),
                    "nounce": "AddQTtkf8DIGC+s9kLxiXg",
                }
            ]
        }
    }