import os
import dotenv

import pytest
import base64

from thechain.app.config import GENESIS_BLOCK
from thechain.app.ingress.service import (
    get_nodes, register_nodes, unregister_nodes, attemp_hangging)
from thechain.app.utils.block_management import create_pow_token
# from thechain.app.egress.solving import (
#     create_pow_token)
from thechain.app.utils.block_management import (
    verify_block_pow)


dotenv.load_dotenv()


def test__solving_main():
    assert verify_block_pow(
        base64.b64decode(
            b"Mjm8bvzdSreeZcLOowQkxtEEVueo6n6Aeqlmz53Njv8=")) == 1


def test__get_nodes():
    assert len(get_nodes()) > 0
    print(get_nodes())
    fakeurl = "https://0.0.0.0:9999"
    register_nodes([fakeurl])
    assert fakeurl in get_nodes()
    unregister_nodes([fakeurl])
    assert fakeurl not in get_nodes()


testcase_block = {
        "pow_token": "7a82hNISXLNsANBp1NsJSLy5vSUJcW4Cy7yA/KmW5iQ=",
        "predicessor": GENESIS_BLOCK,
        "transactions": "test input",
        "proposer_pk": os.getenv("PUBLIC_KEY"),
        "nounce": "AddQTtkf8DIGC+s9kLxiXg==",
         }


def test__attemp_hang_block():
    assert attemp_hangging(testcase_block) == 1


if __name__ == "__main__":
    pytest.main()
