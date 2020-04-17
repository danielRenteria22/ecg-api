USAR LA API LOCALMENTE

Primero se debera instalar:
    -flask
    -pymongo
    -pymodm
    -python-decouple
    -tensorflow
    -Pillow
Y otras cosas que flask te indicara si faltan

Correrlo en modo debug:
sudo FLASK_APP=app.py FLASK_DEBUG=True python -m flask run


*** END POINTS ***
 NOTA: Todas las respuestas del servidor tendran las
 siguiente estructura:
 {
     error: <boolean>,
     message: <String>,
     data: <JsonObject>
 }

error -> indica si hubo algun error en la peticion
message -> mensaje del servidor. Si hubo algun error
aqui estara la causa
data -> la informacion solicitada. Puede ser null

Se puede asumir que todas las respuestras tendran esta estructura

1) /predict

-Espera: 
body = {
   image: <String> 
}

image -> la imagen que se va a evaluar en base64

-Respuesta:
{
    error: <boolean>,
     message: <String>,
     data: {
        resultIndex: <int>,
        result: <String>,
        accuracy: <float>,
        ecg_id: <String>
     }
}

resultIndex-> el index de la prediccion en basae a 
este arreglo ['Non-ecotic beats (normal beat)', 
'Supraventricular ectopic beats',
'Ventricular ectopic beats', 
'Fusion Beats', 
'Unknown Beats']

result -> el resultado en String
accuracy -> la seguridad  de ese resultado (0-1)
ecg_id -> el id en la base de dats de la prediccion. Es
necesario guardarlo para poder calificar la prediccion


2) /rate
- Espera:
body = {
    ecg_id: <String>,
	rating: <boolean>
}
ecg_id -> el id de la prediccion que se quiere calificar
rating -> fue el resultado correcto o normal

- Respuesta:
{
  "data": null,
  "error": <boolean>,
  "message": <string>
}

error -> si fue o no exitosa la calificacion
message -> mensaje del servidor