from datetime import datetime, timedelta

from chatting.db import Session
from chatting.db.models import *


def new_user(user_uuid: str):
    user = User(uuid=user_uuid, time=datetime.today())
    with Session() as session:
        session.query(User).filter(
            User.time < datetime.now() - timedelta(days=3)).delete()
        session.add(user)
        session.commit()


def new_dialog(user_uuid: str, who: int, msg: str, control=False):
    dialog = Dialog(
        uuid=user_uuid, time=datetime.today(), who=who, msg=msg, control_msg=control,
        received=(True if who == 0 else False))
    with Session() as session:
        session.add(dialog)
        session.commit()


def get_dialog(user_uuid: str, all_msg=True):
    with Session() as session:
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
    with Session() as session:
        session.query(Dialog).filter(
            Dialog.time < datetime.now() - timedelta(days=3)).delete()
        session.commit()
        result = session.query(Dialog.msg, Dialog.who).filter(
            Dialog.uuid == user_uuid).all()
        return [{"msg": item[0], "who": item[1]} for item in result]
