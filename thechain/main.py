import threading

import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.egress import endpoints as ed
from app.ingress import endpoints as ine


@asynccontextmanager
async def broadcasting_blocks(app: FastAPI):
    """keep solving puzzles"""
    thread = threading.Thread(
        target=ed.pack_local_known_blocks)
    thread.daemon = True
    thread.start()


@asynccontextmanager
async def solving(app: FastAPI):
    """keep solving puzzles"""
    thread = threading.Thread(
        target=ed.pack_block_attemp)
    thread.daemon = True
    thread.start()


app = FastAPI(
    # lifespan=lifespan,
    redoc_url=None,
    docs_url="/docs",
    title='Ingress of Node',
    # version=,
    description="The APIs of Node Ingress.",
    )


# accept imcomming block
app.include_router(ine.router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7573)
