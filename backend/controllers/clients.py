from sqlalchemy.exc import InvalidRequestError, IntegrityError
from config.DBindex import db_session
from models.client import Clients
from pkg.logger import get_logger as log
from datetime import datetime


def FindAll():
    try:
        query = Clients.query.all()
        dataDict = []
        for data in query:
            data.__dict__.pop("_sa_instance_state")
            dataDict.append(data.__dict__)
        return dataDict, 200
    except Exception as e:
        log().error(e.message)
        return None, 404


def FindOne(cond):
    try:
        query = Clients.query.filter_by(**cond)
        if query.one_or_none() is not None:
            q = query.one_or_none()
            q.__dict__.pop("_sa_instance_state")
            return q.__dict__, 200
        else:
            return None, 404
    except InvalidRequestError:
        log().error("InvalidRequestError")
        return None, 400


def Create(cond):
    createClients = Clients(**cond, create_time=datetime.now())
    
    try:
        db_session.add(createClients)
        db_session.commit()
        return 200
    except InvalidRequestError:
        log().error("Unable to create data")
        return 400
    except IntegrityError:
        log().error("Foreign key not found")
        return 400


def Patch(querys, content):
    try:
        query = Clients.query.filter_by(id=querys).first()
        if query is not None:
            for key in content:
                setattr(query, key, content[key])
            db_session.commit()
            return 200
        else:
            return 404
    except InvalidRequestError:
        log().error("Unable to patch data")
        return 400
