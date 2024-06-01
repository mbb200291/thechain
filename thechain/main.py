import threading

import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager

from thechain.app.egress import endpoints
from thechain.app.ingress import endpoints


@asynccontextmanager
async def lifespan(app: FastAPI):
    """keep solving puzzles"""
    thread = threading.Thread(
        target=endpoints.main)
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
app.include_router(endpoints.router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7573)
