import pytest
import base64

from thechain.app.ingress.modules.block_management import verify_block_pow 
from thechain.app.ingress.modules.block_management import hang_block 


def test__solving_main():
    assert verify_block_pow(
        base64.b64decode(
            b"Mjm8bvzdSreeZcLOowQkxtEEVueo6n6Aeqlmz53Njv8=")) == 1


# def test__hang_block():
#     hang_block(
#         {}
#     )
#     assert True


if __name__ == "__main__":
    pytest.main()
