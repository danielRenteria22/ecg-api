from app import jsonify,Response
from .Utils import MyEncoder



def responde(status,error,message,data):
    responseObject = {
        "error": error,
        "message": message,
        "data": data
    }

    return jsonify(responseObject), status
