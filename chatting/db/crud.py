from random import choice
from datetime import datetime, timedelta

from chatting.db import Session
from chatting.db.models import *


def new_user(user_uuid: str):
    user = User(uuid=user_uuid, time=datetime.today())
    with Session() as session:
        # we should delete the expired user's uuid
        session.query(User).filter(
            User.time < datetime.now() - timedelta(days=3)).delete()
        session.add(user)
        session.commit()
    welcome_msg(user_uuid, True)


def new_dialog(user_uuid: str, who: int, msg: str, control=False):
    dialog = Dialog(
        uuid=user_uuid, time=datetime.today(), who=who, msg=msg, control_msg=control,
        received=(True if who == 0 else False))
    with Session() as session:
        session.add(dialog)
        session.commit()


def welcome_msg(user_uuid: str, first=False):
    msg_list = [
        "Welcome to use chatting! You can chat with Blenderbot, a conversational AI. Besides, you can type \"/clear\" to clear conversation.",
        "Hello, this is chatting! You can chat with a conversational AI called Blenderbot. Have a good time!",
        "Welcome to continue using chatting!",
        "Let's continue chatting!",
        "Hello! It's chatting."
    ]
    if first:
        new_dialog(user_uuid, 1, msg_list[0], True)
    else:
        new_dialog(user_uuid, 1, choice(msg_list[1:]), True)


def get_dialog(user_uuid: str, all_msg=True):
    with Session() as session:
        # the expired dialog should be removed too
        session.query(Dialog).filter(
            Dialog.time < datetime.now() - timedelta(days=3)).delete()
        session.commit()
        if all_msg:
            result = session.query(Dialog.msg).filter(
                Dialog.uuid == user_uuid).all()
        else:
            result = session.query(Dialog.msg).filter(
                Dialog.uuid == user_uuid).filter(Dialog.control_msg == False).all()
        return [item[0] for item in result]


def get_dialog2(user_uuid: str):
    # this function is similar to `get_dialog` but adds
    # some data to identify the person sending the dialog
    with Session() as session:
        session.query(Dialog).filter(
            Dialog.time < datetime.now() - timedelta(days=3)).delete()
        session.commit()
        result = session.query(Dialog.msg, Dialog.who).filter(
            Dialog.uuid == user_uuid).all()
        return [{"msg": item[0], "who": item[1]} for item in result]
