from flask import Flask, request, jsonify,Response
# app = Flask(__name__)


from decouple import config as config_decouple
from config import config
def create_app(enviroment):
    app = Flask(__name__)

    app.config.from_object(enviroment)
    return app

enviroment = config['development']
if config_decouple('PRODUCTION', default=False):
    enviroment = config['production']

app = create_app(enviroment)


@app.route('/')
def index():
    return 'Bienvenido a la API  del projecto MIA'


@app.route('/predict', methods=['GET'])
def predict():
    from controllers.PredictionsController import PredictionsController
    return PredictionsController.predict()

@app.route('/rate', methods=['GET'])
def rate():
    from controllers.PredictionsController import PredictionsController
    return PredictionsController.ratePrediction()