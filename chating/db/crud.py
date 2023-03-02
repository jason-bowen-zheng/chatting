from datetime import datetime, timedelta

from chating.db import Session
from chating.db.models import *


def new_user(user_uuid: str):
    user = User(uuid=user_uuid, time=datetime.today())
    with Session() as session:
        session.query(User).filter(
            User.time <= datetime.now() - timedelta(days=1)).delete()
        session.add(user)
        session.commit()


def get_user(user_uuid: str):
    with Session() as session:
        result = session.query(User).filter(User.uuid == user_uuid).all()
    if len(result) == 0:
        return
    else:
        return result[0]


def new_dialog(user_uuid: str, who: int, msg: str, control=False):
    dialog = Dialog(
        uuid=user_uuid, time=datetime.today(), who=who, msg=msg, control_msg=control,
        received=(True if who == 0 else False))
    with Session() as session:
        session.add(dialog)
        session.commit()


def get_dialog(user_uuid: str):
    with Session() as session:
        session.query(Dialog).filter(
            Dialog.time <= datetime.now() - timedelta(weeks=1)).delete()
        session.commit()
        result = session.query(Dialog.msg).filter(
            Dialog.uuid == user_uuid).all()
        return [item[0] for item in result]
