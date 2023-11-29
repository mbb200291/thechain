import threading

import uvicorn
from fastapi import FastAPI

from app.egress import solving
from app.ingress import routers


app = FastAPI(
    redoc_url=None,
    docs_url="/docs",
    title='Ingress of Node',
    # version=,
    description="The APIs of Node Ingress.",
    )

# solve
@app.lifespan("startup")
def start_scheduler():
    thread = threading.Thread(
        target=solving.main)
    thread.daemon = True
    thread.start()
    
    
# accept imcomming block
app.include_router(routers.router)



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
