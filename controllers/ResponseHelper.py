from app import jsonify,Response



def responde(status,error,message,data):
    responseObject = {
        "error": error,
        "message": message,
        "data": data
    }
    
    return responseObject, status
