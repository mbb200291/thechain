import os
import base64

import dotenv

dotenv.load_dotenv()


# TAU = 128
TAU = 3
SEED_URLS = ['http://localhost:7573']
GENESIS_BLOCK = "thegenesisblock="
PUBLIC_KEY =  base64.b64decode(os.getenv("PUBLIC_KEY").encode('ascii'))
