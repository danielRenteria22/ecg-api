from flask import Flask, request, jsonify,Response
import tensorflow.keras as keras
import tensorflow as tf
import numpy as np
from pymodm import connect, fields, MongoModel, EmbeddedMongoModel
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

# connect('mongodb://localhost:27017/ezECG')
connect('mongodb://danielRenteria22:3838380814@cluster0-shard-00-00-wtqqx.mongodb.net:27017/mydb,cluster0-shard-00-01-wtqqx.mongodb.net:27017/mydb,cluster0-shard-00-02-wtqqx.mongodb.net:27017/mydb?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority')
ecgModel = tf.keras.models.load_model('ecg.model')
labels = ['Non-ecotic beats (normal beat)', 
'Supraventricular ectopic beats',
'Ventricular ectopic beats', 
'Fusion Beats', 
'Unknown Beats']

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