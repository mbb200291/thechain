import os
import base64
import pathlib

import dotenv

from .utils import block_management

dotenv.load_dotenv()


# TAU = 128
# TAU = 10
# TAU = 7
TAU = 11
SEED_IPS = ['http://localhost:7573']
# GENESIS_BLOCK = "thegenesisblock"
GENESIS_BLOCK = "thegenesisblock="
# PUBLIC_KEY =  base64.b64decode(os.getenv("PUBLIC_KEY", "").encode('ascii'))
PUBLIC_KEY =  os.getenv("PUBLIC_KEY", "")
DBPATH = os.getenv("DBPATH") if os.getenv("DBPATH") is not None else pathlib.Path(__file__).parent / 'utils' /  'theblock.sqlite'
# DBPATH = # flaskbb