from flask import Flask, request, jsonify
import flask
from flask_cors import CORS 
from pruebasistema import buscarTweets, datosGrafica

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/pedir', methods=['GET','POST'])
def extract_tweets():
    content= request.get_json()
    palabraClave=content['palabraBusqueda']
    hashtagClave=content['hashtagBusqueda']
    usuarioClave=content['usuarioBusqueda']
    fechaMin=content['fechaMinBusqueda']
    cercania=content['cercaniaBusqueda']

    print(palabraClave)
    print(hashtagClave)
    print(usuarioClave)
    print(fechaMin)
    print(cercania)
    nueva_consulta=buscarTweets(palabraClave,hashtagClave,usuarioClave,fechaMin,cercania)

    datos_grafica=datosGrafica(nueva_consulta)

    return datos_grafica

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)