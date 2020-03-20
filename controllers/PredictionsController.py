from app import jsonify,request,Response
import random

class PredictionsController :
    @staticmethod
    def predict():
        request.get_json(force=True)
        image = request.json.get("image")
        if not image:  return Response("No image was sent",status=400)

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

        return jsonify(response)

    @staticmethod
    def ratePrediction():
        request.get_json(force=True)
        prediction_id = request.json.get("prediction_id")
        rating = request.json.get("rating")

        if not prediction_id: return Response("No prediction was sent",status=400)
        print(not isinstance(rating, bool))
        if (not rating) or (not isinstance(rating, bool)): return Response("Uniexisting or invalid rating",status=400)

        # Parametro dummy para probar si la evualuacion fue exitosa
        successful =  request.json.get("successful")

        if successful:
            return Response("Rating was succesful",status=200)
        else:
            return Response("Rating was not succesful",status=400)
