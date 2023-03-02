from os import path
from threading import Thread
from typing import Union
from uuid import uuid4

from fastapi import Cookie, FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from chating.api import api_router
from chating.db.crud import *
from chating.ai.blenderbot import generate_loop, msg_queue

app = FastAPI(docs_url=None, redoc_url=None)
app.include_router(api_router)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def index(uuid: Union[str, None] = Cookie(default=None)):
    html = open(path.join(path.dirname(__file__), "index.html"), "r").read()
    response = HTMLResponse(html)
    if uuid is None:
        user_id = uuid4().hex
        new_user(user_id)
        response.set_cookie("uuid", user_id, expires=3600 * 24)
    return response


@app.on_event("startup")
def startup():
    Thread(target=generate_loop).start()


@app.on_event("shutdown")
def shutdown():
    msg_queue.put(("system", "shutdown"))
