# import threading

# import uvicorn
# from fastapi import FastAPI
# from contextlib import asynccontextmanager

# import thechain.app.egress.endpoints as ege
# import thechain.app.ingress.endpoints as ige


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     """keep solving puzzles"""
#     thread = threading.Thread(
#         target=ege.router)
#     thread.daemon = True
#     thread.start()


# app = FastAPI(
#     lifespan=lifespan,
#     redoc_url=None,
#     docs_url="/docs",
#     title='Ingress of Node',
#     # version=,
#     description="The APIs of Node Ingress.",
#     )


# # accept imcomming block
# app.include_router(ige.router)


# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=7573)
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("ing")
args = parser.parse_args()
print(args.echo)
