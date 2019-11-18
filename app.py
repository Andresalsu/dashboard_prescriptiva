import flask
from flask import Flask, render_template, request, jsonify, send_file, send_from_directory, safe_join, abort
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from pruebasistema import buscarTweets
import json, os, psycopg2

app = Flask(__name__)
CORS(app)

PSQL_HOST = "192.168.96.38"
PSQL_PORT = "5432"
PSQL_USER = "loken"
PSQL_PASS = "s3cur1ty"
PSQL_DB = "prescriptiva"

app.config["CLIENT_CSV"] = "./csv"

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/pedir', methods=['GET','POST'])
def extract_tweets():
    #Se solicitan las variables para buscar los tweets
    content= request.get_json()
    palabraClave=content['palabraBusqueda']
    hashtagClave=content['hashtagBusqueda']
    usuarioClave=content['usuarioBusqueda']
    fechaMin=content['fechaMinBusqueda']
    cercania=content['cercaniaBusqueda']

    #Se envia la consulta al script pruebasistema.py
    nueva_consulta=buscarTweets(palabraClave,hashtagClave,usuarioClave,fechaMin,cercania)

    #Se devuelven los resultados de todos los tweets encontrados
    with open('data.json','r') as f:
        return json.loads(f.read())

@app.route('/obtener', methods=['GET','POST'])
def return_stats():
    #Metodo para devolver resultados en cualquier momento (Asincronamente)
    with open('data.json','r') as f:
        return json.loads(f.read())

#-------Consultar Archivos por usuario-------------------------
#Metodo que consulta los archivos asociados a un usuario determinado
#Recibe el nombre por medio de un json del usuario para realizar la busqueda respectiva en la base de datos y retornas la lista de archivo
#El metodo retorna la lista de archivos asociados al usuario en un Json
@app.route('/consultar', methods=['POST'])
def consultar():

    content = request.get_json()
    nombres = content['nombre']

    connstr = "host=%s port=%s user=%s password=%s dbname=%s" % (
        PSQL_HOST, PSQL_PORT, PSQL_USER, PSQL_PASS, PSQL_DB)
    conn = psycopg2.connect(connstr)

    cur = conn.cursor()

    sqlquery = "select usuario.id from usuario where usuario.nombre="+"'"+nombres+"'"+";"
    cur.execute(sqlquery)
    row_headers = [x[0] for x in cur.description]
    row = cur.fetchone()
    sqlquerys = "select archivo.url from archivo where archivo.id_user="+"'"+str(row[0])+"'"+";"
    cur.execute(sqlquerys)
    row1=cur.fetchall()
    payload = []
    content = {}
    for result in row1:
        content = {'url': result[0],
                   }
        payload.append(content)
        content = {}
    cur.close()
    conn.close()

    return jsonify(payload)

##--------------------------Insertar Usuario en base de datos------------------#
##Inserta un usuario en la base de datos
#@param nombres: parametro que hace referencia al nombre del usuario que viene por medio del json
#@param correos: parametro que hace referencia al correo del  usuario que viene por medio del json
#@param passwords: parametro que hace referencia al password del  usuario que viene por medio del json
#@return: retorna un json con valor success si todo funcionó correctamente
@app.route('/insertarUsuario', methods=['POST'])
def insertar():
    content = request.get_json()
    nombres = content['nombre']
    correos = content['correo']
    passwords = content['password']
    connstr = "host=%s port=%s user=%s password=%s dbname=%s" % (
        PSQL_HOST, PSQL_PORT, PSQL_USER, PSQL_PASS, PSQL_DB)
    conn = psycopg2.connect(connstr)

    cur = conn.cursor()

    sqlquery = "INSERT INTO usuario(nombre, correo, password, id)VALUES (" + "'" + \
        nombres+"'"+"," + "'"+correos+"'" + ","+"'" + passwords+"'"+", default);"
    cur.execute(sqlquery)
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"Value": "succes"})

##--------------------------Insertar Archivo en base de datos------------------#
##Inserta el nombre del archivo asociado al usuario
#@param nombres: parametro que hace referencia al nombre del usuario que viene por medio del json
#@param nombreFile: parametro que hace referencia al nombre del archivo por el que se desea concultar 
#@return: retorna un json con valor succesFull si todo funcionó correctamente
@app.route('/insertarArchivo', methods=['POST'])
def insertarArchivo():
    content = request.get_json()
    nombres = content['nombre']
    nombreFile = content['nombreFile']
    connstr = "host=%s port=%s user=%s password=%s dbname=%s" % (
        PSQL_HOST, PSQL_PORT, PSQL_USER, PSQL_PASS, PSQL_DB)
    conn = psycopg2.connect(connstr)

    cur = conn.cursor()
    sqlquery = "select usuario.id from usuario where usuario.nombre="+"'"+nombres+"'"+";"
    cur.execute(sqlquery)

    row_id = cur.fetchone()
    sqlquerys = "INSERT INTO archivo(url, id_user)VALUES (" + \
        "'"+nombreFile+"'"+"," + "'"+str(row_id[0])+"'"+");"
    cur.execute(sqlquerys)
    conn.commit()

    cur.close()
    conn.close()
    return jsonify({"state": "Successfull"})

##--------------------------Verificar usuario------------------#
##Verifica si existe un usuario registrado en la base de datos, atraves de la clave encriptada
#@param password: parametro que hace referencia a la clave  del usuario que viene por medio del json
#@param correo: parametro que hace referencia al correo del usuario en la base de datos y viene atarves de un json 
#@return: retorna un json con valor succesFull si todo funcionó correctamente
@app.route('/verificarUsuario', methods=['POST'])
def verificarUsuario():
    content = request.get_json()
    passwords = content['password']
    correos=content['correo']
    connstr = "host=%s port=%s user=%s password=%s dbname=%s" % (
        PSQL_HOST, PSQL_PORT, PSQL_USER, PSQL_PASS, PSQL_DB)
    conn = psycopg2.connect(connstr)
    try:

        cur = conn.cursor()
        sqlquery = "select usuario.id, usuario.nombre, usuario.password from usuario where usuario.password="+"'"+passwords+"'"+ "AND usuario.correo="+"'"+correos+"'"+ ";"
        cur.execute(sqlquery)
        rows = cur.fetchone()

        if str(rows[2]== passwords):

            return jsonify({"state": "Successfull", "nombre": rows[1], "id": rows[0]})
        
    except:
         return jsonify({"state": "Failed"})

##--------------------------Descargar Archivo del servidor------------------#
##Descarga un archivo disponible en el servidor que está asociado a un usuario
#El nombre del archivo ingresa atraves de una URL de la siguiente forma  http://<host>:<port>/get-image/<nombreArchivo>
#@return: permite retornar el archivo automaticamente una vez se consumaa el servicio 
@app.route("/get-csv/<csv_id>")
def get_csv(csv_id):

    filename = f"{csv_id}.csv"

    try:
        return send_from_directory(
            app.config["CLIENT_CSV"], filename=filename, as_attachment=True)
    except :
        return jsonify({"state": "failed"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5002, debug=True)
    app.secret_key = os.urandom(24)