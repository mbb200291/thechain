import threading

import uvicorn
from fastapi import FastAPI

from app.ingress import endpoints as ine


app = FastAPI(
    redoc_url=None,
    docs_url="/docs",
    title='Ingress of Node',
    description="The APIs of Node Ingress.",
    )


# accept imcomming block
app.include_router(ine.router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7573)
