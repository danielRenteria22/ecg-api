from app import request,ecgModel,np,labels,jsonify
from .ResponseHelper import responde
from models.UserEcg import UserEcg
from datetime import date

class PredictionsController :
    @staticmethod
    def predict():
        from .UserController import UserController
        request.get_json(force=True)
        base64Raw = request.json.get("image")
        if not base64Raw:  return responde(400,True,"No image was sent",None)
        
        try:
            base64Array = base64Raw.split(',')
            base64 = base64Array[len(base64Array) - 1]
            image = PredictionsController.base64ToImage(base64)
            points = PredictionsController.getSamplepoints(image)
            x_predict = np.asarray(points)
            predictions = ecgModel.predict(np.asarray([x_predict]))
            indexMax = np.argmax(predictions[0])

            currentUser = UserController.userFromSession()
            userId = None
            if currentUser:
                userId = currentUser._id

            new_ecg = UserEcg(
                    points,
                    indexMax,
                    date.today(),
                    None,
                    'some_url',
                    userId,
                    'TRAINING'
                ).save()

            response = {
                "resultIndex": int(indexMax),
                "result": labels[indexMax],
                "accuracy": float(predictions[0][indexMax]),
                "ecg_id": str(new_ecg._id)
            }



            return responde(200,False,"Prediction was successful",response) 
        except Exception, e:
            return responde(500,True,'Prediction failed',str(e))

    @staticmethod
    def ratePrediction():
        from bson.objectid import ObjectId   
        request.get_json(force=True)
        prediction_id = request.json.get("ecg_id")
        rating = bool(request.json.get("rating"))

        if not prediction_id: return responde(400,True,"No prediction id",None)
        if rating == None: return responde(400,True,'No rating was provided',None)

        try:  
            userEcg =  UserEcg.objects.raw({'_id': ObjectId(prediction_id)})[0]
            userEcg.correct_classification = rating
            userEcg.save()
            return responde(200,False,'Rating was succesful',None)
        except:
            return responde(404,True,'ECG was not found',None)

        

    @staticmethod
    def base64ToImage(data):
        from PIL import Image
        from io import BytesIO
        import base64

        return Image.open(BytesIO(base64.b64decode(str(data))))


    @staticmethod
    def getSamplepoints(image):
        from scipy.interpolate import interp1d
        sample_size = 100
        thresh_hold = 170

        pixels = image.load()

        width = image.size[0]
        heigth = image.size[1]
        jump_size = int(width / sample_size)
        sample_points = []
        min_heigth = 0
        max_heigth = 0
        is_first = True
        finish = False

        for x in range(0,width,jump_size):
            found = False
            for y in range(heigth):
                current_pixel = pixels[x,y]
                if(current_pixel[0] < thresh_hold and current_pixel[1] < thresh_hold and current_pixel[2] < thresh_hold):
                    found = True
                    y = heigth -y
                    if(is_first):
                        min_heigth = y
                        max_heigth = x
                        is_first = False
                    else:
                        if(y < min_heigth):
                            min_heigth = y
                        elif(y > max_heigth):
                            max_heigth = y
                        
                    sample_points.append(y)
                    break
            if not found: 
                print('Point not found in x =' + str(x))
                currentIndex = len(sample_points) - 1
                if currentIndex >= 2:
                    a = sample_points[currentIndex - 1]
                    b = sample_points[currentIndex - 2]
                    sample_points.append(a + ((a-b) / 2))
                else:
                    sample_points.append(heigth / 2)
            if(len(sample_points) == sample_size): break
            if int(x / jump_size) >= sample_size + 1: break

        interpolator = interp1d([min_heigth,max_heigth],[0,1])
        interpolated_points = []
        for point in sample_points:
            inter_point = float(interpolator(point))
            interpolated_points.append(inter_point)

        return interpolated_points

    
