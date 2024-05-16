from pydantic import BaseModel, HttpUrl


# class IpList(BaseModel):
#     ips: list[str]

# class IPs(BaseModel):
#     ip: list[HttpUrl]


class Block(BaseModel):
    pow_token: str  # base64 encoded of sha256([md5(block_content, 128bits, 16bytes)] | md5(predicessor, 128bits, 16bytes) | md5(proposer_pk, 128, 16bytes)] | nounce (128, 16bytes)]) """
    block_content: str
    predicessor: str  # pow_token of predicessor
    proposer_pk: str  # public key (PEM format) (base64 encoded)
    nounce: str  # base64 encoded nounce bytes
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "pow_token": "ifijefjlfdjf",
                    "block_content": "test content",
                    "predicessor": "dfdfeijoei",
                    "proposer_pk": "dfdfdf",
                    "nounce": "dfmfmioief"
                }
            ]
        }
    }