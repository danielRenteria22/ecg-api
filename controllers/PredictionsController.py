from app import request
from .ResponseHelper import responde
import random

class PredictionsController :
    @staticmethod
    def predict():
        request.get_json(force=True)
        image = request.json.get("image")
        if not image:  return responde(400,True,"No image was sent",None)

        # TODO Resultados dummies, se va a pedir el resulrado que
        # que se quiera obtener. Borrar

        # TODO se necesiua una manera de guardar una imagen en un bucket 
        # para solo tener que almacenar la url de la imagen en vez de la
        # imagen completa
        #  
        expected = request.json.get("expected")
        response = {
            "result": expected,
            "accuracy": random.random() * 20 + 80,
            "prediction_id": random.randint(100,10000)
        }

        return responde(200,False,"Prediction was successful",response)

    @staticmethod
    def ratePrediction():
        request.get_json(force=True)
        prediction_id = request.json.get("prediction_id")
        rating = bool(request.json.get("rating"))

        if not prediction_id: return responde(400,True,"No prediction id",None)

        # Parametro dummy para probar si la evualuacion fue exitosa
        successful =  request.json.get("successful")

        if successful:
            return responde(200,False,"Rating was sucessful",None)
        else:
            return responde(400,True,"Rating was not successful",None)
