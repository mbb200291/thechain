import asyncio

from app.egress import endpoints as ed

async def main():
    await ed.pack_block_attemp()
    await ed.pack_local_known_blocks()
    # await ed.test_broadcast()


if __name__ == "__main__":
    asyncio.run(main())
