import os
import base64

import dotenv

from .utils import block_management

dotenv.load_dotenv()


# TAU = 128
TAU = 10
SEED_URLS = ['http://localhost:7573']
# GENESIS_BLOCK = "thegenesisblock"
GENESIS_BLOCK = "thegenesisblock="
# PUBLIC_KEY =  base64.b64decode(os.getenv("PUBLIC_KEY", "").encode('ascii'))
PUBLIC_KEY =  os.getenv("PUBLIC_KEY", "")
