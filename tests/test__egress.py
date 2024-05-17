import os

import pytest
import dotenv
import base64

from thechain.app.egress.solving import (
    create_pow_token, GENESIS_BLOCK, create_nounce, 
    )


dotenv.load_dotenv()


def test__get_ips():
    assert True


def test__extend_ips():
    assert True


def test__create_block():
    powtoken = create_pow_token(
            GENESIS_BLOCK,
            "test input",
            os.getenv("PRIVATEKEY"),
            base64.b64encode(b"AddQTtkf8DIGC+s9kLxiXg==")
        )
    # print("nounce:", base64.b64encode(create_nounce()))
    # print("nounce:", "AddQTtkf8DIGC+s9kLxiXg==")
    # print(powtoken)
    print("pow(b64):", base64.b64encode(powtoken))
    assert powtoken != ''


if __name__ == "__main__":
    pytest.main()
