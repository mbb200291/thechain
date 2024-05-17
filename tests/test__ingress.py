import os
import dotenv

import pytest
import base64

from thechain.app.config import GENESIS_BLOCK
from thechain.app.ingress.service import (
    get_nodes, register_nodes, unregister_nodes, attemp_hangging)
from thechain.app.egress.solving import (
    create_pow_token)
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


def test__attemp_hang_block():
    assert attemp_hangging({
        "pow_token": "sAtrhS4uH+uFFrdXWyR1kA0jKY/ubNB7Er2Jg1NF2fk=",
        "predicessor": GENESIS_BLOCK,
        "block_content": "test input",
        "proposer_pk": os.getenv("PRIVATEKEY"),
        "nounce": "AddQTtkf8DIGC+s9kLxiXg==",
         }) == 1


if __name__ == "__main__":
    pytest.main()
