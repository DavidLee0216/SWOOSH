from sqlalchemy.exc import InvalidRequestError, IntegrityError
from config.DBindex import db_session
from models.order import ClientOrders
from pkg.logger import get_logger as log
from datetime import datetime
from pkg.checkDictMatch import checkDictKeyMatchArray


modelKey = [
    "id",
    "satellite_name" ,
    "weight_kg" ,
    "purpose" ,
    "request_by" ,
    "eta_height_km" ,
    "arrival_date" ,
    "inclination" ,
    "budget_billion" 
]

def FindAll():
    try:
        query = ClientOrders.query.all()
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
        querydict, isMatch = checkDictKeyMatchArray(modelKey, cond)
        if not isMatch or not 'id' in querydict:
            return None, 400
        query = ClientOrders.query.filter_by(**querydict).one_or_none()

        if query is not None:
            query.__dict__.pop("_sa_instance_state")
            return query.__dict__, 200
        else:
            return None, 404
    except InvalidRequestError:
        log().error("InvalidRequestError")
        return None, 400


def Create(cond):
    querydict = {}
    querydict, isMatch = checkDictKeyMatchArray(modelKey, cond)
    if not isMatch:
        return None, 400

    createClientOrder = ClientOrders(**querydict)
    
    try:
        db_session.add(createClientOrder)
        db_session.commit()
        return querydict, 200
    except InvalidRequestError:
        log().error("Unable to create data")
        return None, 400
    except IntegrityError:
        log().error("Foreign key not found")
        return None, 400


def Patch(content):
    try:
        querydict, isMatch = checkDictKeyMatchArray(modelKey, content)
        if not isMatch:
            return None, 400
        query = ClientOrders.query.filter_by(id=content.pop("id")).one_or_none()
        if query is not None:
            
            for key in querydict:
                setattr(query, key, querydict[key])
            db_session.commit()
            return querydict, 200
        else:
            return None, 404
    except InvalidRequestError:
        log().error("Unable to patch data")
        return None, 400

def Delete(id):
    try:
        toDel = ClientOrders.query.filter_by(id=id).first()
        if toDel is not None:
            db_session.delete(toDel)
            db_session.commit()
            return 200
        else:
            return 400
    except InvalidRequestError:
        log().error("Unable to delete data")
        return 400