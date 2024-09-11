import threading

from app.egress import endpoints as ed


if __name__ == "__main__":
    ed.pack_block_attemp()
    ed.pack_local_known_block
