from app import jsonify,Response

@staticmethod
    def responde(status: int,error: bool,message: str,data: object):
        response = jsonify({
            "error": error,
            "message": message,
            "data": data
        })

        return Response(response,status=status)
