import os

import pytest
import dotenv
import base64

from thechain.app.utils.block_management import create_nounce, create_pow_token
from thechain.app.config import GENESIS_BLOCK
from thechain.app.egress.modules.broadcasting import broadcast


dotenv.load_dotenv()


def test__create_block():
    powtoken = create_pow_token(
            "test input".encode('utf8'),
            base64.b64decode(GENESIS_BLOCK.encode('ascii')),
            base64.b64decode(os.getenv("PRIVATEKEY").encode('ascii')),
            base64.b64decode(b"AddQTtkf8DIGC+s9kLxiXg==")
        )
    # print("pow(b64):", base64.b64encode(powtoken).decode('ascii'))
    assert powtoken == b'7a82hNISXLNsANBp1NsJSLy5vSUJcW4Cy7yA/KmW5iQ='

def test__broadcast_block():
    block = guess
    broadcast()

if __name__ == "__main__":
    pytest.main()
