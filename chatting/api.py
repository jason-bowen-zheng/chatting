from fastapi import APIRouter, Cookie, Depends, HTTPException, status
from pydantic import BaseModel

from chatting.ai.blenderbot import msg_queue
from chatting.db import Session
from chatting.db.crud import *
from chatting.db.models import *

api_router = APIRouter(prefix="/api")


class MsgModel(BaseModel):
    msg: str


def verify_cookie(uuid: str = Cookie(default="")):
    with Session() as session:
        result = session.query(User).filter(User.uuid == uuid).all()
        if len(result) == 0:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="user not found")


@api_router.post("/new_msg", dependencies=[Depends(verify_cookie)])
def new_msg(data: MsgModel, uuid: str = Cookie(default="")):
    new_dialog(uuid, 0, data.msg)
    msg_queue.put((uuid, data.msg))
    return {"success": 1}


@api_router.get("/get_history", dependencies=[Depends(verify_cookie)])
def get_history(uuid: str = Cookie(default="")):
    with Session() as session:
        session.query(Dialog).filter(
            Dialog.uuid == uuid).update({"received": True})
        session.commit()
        return get_dialog2(uuid)


@api_router.get("/clear_history", dependencies=[Depends(verify_cookie)])
def clear_history(uuid: str = Cookie(default="")):
    with Session() as session:
        session.query(Dialog).filter(Dialog.uuid == uuid).delete()
        session.commit()
        return {"success": 1}


@api_router.get("/get_response", dependencies=[Depends(verify_cookie)])
def get_response(uuid: str = Cookie(default="")):
    with Session() as session:
        result = session.query(Dialog).filter(Dialog.uuid == uuid).filter(
            Dialog.who == 1).filter(Dialog.received == False).all()
        if len(result) == 0:
            return {"responsed": -1}
        else:
            session.query(Dialog).filter(Dialog.uuid == uuid).filter(
                Dialog.who == 1).filter(Dialog.received == False).update({"received": True})
            session.commit()
            return {"responsed": 1, "msg": result[-1].msg}
