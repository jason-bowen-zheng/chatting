from os import path
from threading import Thread
from typing import Union
from uuid import uuid4

from fastapi import Cookie, FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from chatting.ai.blenderbot import generate_loop, msg_queue
from chatting.api import api_router
from chatting.db.crud import *

app = FastAPI(docs_url=None, redoc_url=None)
app.include_router(api_router)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def index(uuid: Union[str, None] = Cookie(default=None)):
    html = open(path.join(path.dirname(__file__), "index.html"), "r").read()
    response = HTMLResponse(html)
    if uuid is None:
        # we use a cookie to differentiate between users
        user_uuid = uuid4().hex
        new_user(user_uuid)
        response.set_cookie("uuid", user_uuid, expires=3600 * 24 * 3)
    return response


@app.on_event("startup")
def startup():
    Thread(target=generate_loop).start()


@app.on_event("shutdown")
def shutdown():
    msg_queue.put(("system", "shutdown"))
