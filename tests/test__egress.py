import os

import pytest
import dotenv
import base64

from thechain.app.utils.block_management import create_nounce, create_pow_token
from thechain.app.config import GENESIS_BLOCK
from thechain.app.egress.modules.broadcasting import broadcast
from thechain.app.egress.endpoints import pack_block_attemp


dotenv.load_dotenv()


def test__create_block():
    powtoken = create_pow_token(
            "test input".encode('utf8'),
            base64.b64decode(GENESIS_BLOCK.encode('ascii')),
            base64.b64decode(os.getenv("PUBLIC_KEY").encode('ascii')),
            base64.b64decode(b"AddQTtkf8DIGC+s9kLxiXg==")
        )
    print("pow(b64):", base64.b64encode(powtoken).decode('ascii'))
    assert base64.b64encode(powtoken).decode('ascii') == '7a82hNISXLNsANBp1NsJSLy5vSUJcW4Cy7yA/KmW5iQ='
    # assert True


def test__pack_block():
    pow = pack_block_attemp()   # TODO: test this
    print(pow)
    assert pow


if __name__ == "__main__":
    pytest.main()
