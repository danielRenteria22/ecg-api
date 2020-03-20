from flask import Flask, request, jsonify,Response
app = Flask(__name__)

from controllers.PredictionsController import PredictionsController


@app.route('/')
def index():
    return 'Bienvenido a la API  del projecto MIA'


@app.route('/predict', methods=['GET'])
def predict():
    return PredictionsController.predict()

@app.route('/rate', methods=['GET'])
def rate():
    return PredictionsController.ratePrediction()