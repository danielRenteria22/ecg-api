from app import request,labels,jsonify
from .ResponseHelper import responde
from .UserController import UserController
from models.ECGModel import ECGModel
import random
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import base64
from io import BytesIO
from datetime import date

class TestController: 

    @staticmethod
    def generateTest():
        user = UserController.userFromSession()
        if not user: return responde(401,True,'You must be log in to take the test',None)

        traningEcg = []
        for e in ECGModel.objects.raw({'use': 'TRAINING'}):
            traningEcg.append(e)

        testCases = []
        for i in range(0,5):
            print(len(traningEcg))
            testIndex = random.randint(0,len(traningEcg) - 1)
            testCases.append(traningEcg[testIndex])
        traningEcg = []

        test = []
        for case in testCases:
            image = TestController.getImageFromPoints(case.points)
            currTest = {
                'image': image,
                'id': str(case._id)
            }
            test.append(currTest)

        return responde(200,False,'Test created',test)

    @staticmethod
    def gradeTest():
        from bson.objectid import ObjectId
        user = UserController.userFromSession()
        if not user: return responde(401,True,'You must be log in to take the test',None)

        request.get_json(force=True)
        answers = list(request.json.get('answers'))
        
        try:
            for answer in answers:
                currEcg = ECGModel.objects.raw({'_id': ObjectId(answer['id'])})[0]
                if answer['category'] != currEcg.category: return responde(200,True,'One or more answers were incorrect',None)
        except Exception as e:
            return responde(404,True,'One or more of the ecg doenst exist: ' + str(e),None)

        # Si llego aqui, significa que todas las respuestas fueron correctas
        user.isAuthorized = True
        user.save()
        return responde(200,False,'User is now authorized',user.toJson())



    
    @staticmethod
    def getImageFromPoints(points):
        matplotlib.use('Agg')
        figure = plt.figure()
        plot = figure.add_subplot (111)
        plot.plot(points)

        return TestController.dataToImage(figure)

    
    @staticmethod
    def plotToData(fig):
        fig.canvas.draw()
    
        # Get the RGBA buffer from the figure
        w,h = fig.canvas.get_width_height()
        buf = np.fromstring ( fig.canvas.tostring_argb(), dtype=np.uint8 )
        buf.shape = ( w, h,4 )
    
        # canvas.tostring_argb give pixmap in ARGB mode. Roll the ALPHA channel to have it in RGBA mode
        buf = np.roll ( buf, 3, axis = 2 )
        return buf

    @staticmethod
    def dataToImage(fig):
        # put the figure pixmap into a numpy array
        buf = TestController.plotToData ( fig )
        w, h, d = buf.shape
        image = Image.frombytes( "RGBA", ( w ,h ), buf.tostring( ) )

        buffered = BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue())

        return img_str
