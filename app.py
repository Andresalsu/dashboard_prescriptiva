import flask
from flask import Flask, render_template, request, jsonify, send_file, send_from_directory, safe_join, abort
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from pruebasistema import buscarTweets
import json, os, psycopg2, base64, time, datetime

app = Flask(__name__)
CORS(app)

PSQL_HOST = "prescriptiva.cwb5ajusgrsr.us-east-1.rds.amazonaws.com"
PSQL_PORT = "5432"
PSQL_USER = "carvajal"
PSQL_PASS = "Carvajal2019"
PSQL_DB = "prescriptiva"

app.config["CLIENT_CSV"] = "./csv"
app.config["CLIENT_JSON"] = "./historic"

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
    correo = content['correo']

    connstr = "host=%s port=%s user=%s password=%s dbname=%s" % (
        PSQL_HOST, PSQL_PORT, PSQL_USER, PSQL_PASS, PSQL_DB)
    conn = psycopg2.connect(connstr)

    cur = conn.cursor()
    #Se envia la consulta al script pruebasistema.py
    nueva_consulta=buscarTweets(palabraClave,hashtagClave,usuarioClave,fechaMin,cercania)

    #Se devuelven los resultados de todos los tweets encontrados
    sqlquery = "select usuario.id from usuario where usuario.correo="+"'"+correo+"'"+";"
    cur.execute(sqlquery)
    conn.commit()

    row_id = cur.fetchone()

    data = ''
    with open('data.json','r',encoding='utf-8') as f:
        data=json.loads(f.read())
    with open("./historic/"+nueva_consulta+".json",'a+',encoding='utf-8')as fl:
        fl.write(data+'\n')
    
    sqlquery = "select archivo.json from archivo where archivo.id_user="+"'"+str(row_id[0])+"'"+";"
    cur.execute(sqlquery)
    conn.commit()

    row=cur.fetchone()
    try:
        if(row[0] is nueva_consulta.replace('.csv','')):
            sqlquery = "UPDATE archivo SET archivo.json='"+nueva_consulta.replace('.csv','')+".json' WHERE archivo.id_user="+str(row_id[0])+";"
            cur.execute(sqlquery)
            conn.commit()
    except:
        sqlquery = "INSERT INTO archivo(url,id_user,json,fecha)VALUES (" + "'" + \
                        nueva_consulta.replace('.csv','')+"'"+"," + "'"+str(row_id[0])+"'"+",'"+nueva_consulta.replace('.csv','')+"','"+ \
                        str(datetime.datetime.now())+"');"
        cur.execute(sqlquery)
        conn.commit()

    cur.close()
    conn.close()

    return data

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

    try:
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
        sqlquerys = "select archivo.url, archivo.fecha from archivo where archivo.id_user="+"'"+str(row[0])+"'"+";"
        cur.execute(sqlquerys)
        row1=cur.fetchall()
        payload = []
        content = {}
        for result in row1:
            content = {'url': result[0], 'fecha': result[1]
                    }
            payload.append(content)
            content = {}
        cur.close()
        conn.close()

        return jsonify(payload)
    except Exception as e:
        print(e)
        return jsonify([{'url':"Not Found"}])

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
    try:
        if(nombres is not '' and correos is not '' and passwords is not ''):
            sqlquery = "select usuario.id from usuario where usuario.correo="+"'"+correos+"'"+";"
            cur.execute(sqlquery)

            row=cur.fetchone()

            if not row:
                sqlquery = "INSERT INTO usuario(nombre, correo, password, id)VALUES (" + "'" + \
                    nombres+"'"+"," + "'"+correos+"'" + ","+"'" + passwords+"'"+", (SELECT MAX(id)+1 FROM usuario));"
                cur.execute(sqlquery)
                conn.commit()
                cur.close()
                conn.close()
                return jsonify({"Value": "success"})
            else:
                cur.close()
                conn.close()
                return jsonify({"Value": "exist"})
        else:
            raise Exception
    except Exception as e:
        print(e)
        return jsonify({"Value": "failed"})

##--------------------------Insertar Archivo en base de datos------------------#
##Inserta el nombre del archivo asociado al usuario
#@param nombres: parametro que hace referencia al nombre del usuario que viene por medio del json
#@param nombreFile: parametro que hace referencia al nombre del archivo por el que se desea concultar 
#@return: retorna un json con valor succesFull si todo funcionó correctamente
@app.route('/insertarArchivo', methods=['POST'])
def insertarArchivo():
    try:
        content = request.get_json()
        nombres = content['nombre']
        nombreFile = content['nombreFile']
        connstr = "host=%s port=%s user=%s password=%s dbname=%s" % (
            PSQL_HOST, PSQL_PORT, PSQL_USER, PSQL_PASS, PSQL_DB)
        conn = psycopg2.connect(connstr)

        cur = conn.cursor()

        if(nombres is not '' and nombreFile is not ''):
            sqlquery = "select usuario.id from usuario where usuario.nombre="+"'"+nombres+"'"+";"
            cur.execute(sqlquery)

            row_id = cur.fetchone()

            sqlquery = "select archivo.id_user from archivo where archivo.url="+"'"+nombreFile+"'"+";"
            cur.execute(sqlquery)

            row=cur.fetchone()

            if not row:
                sqlquerys = "INSERT INTO archivo(url,id_user,json,fecha)VALUES (" + "'" + \
                        nombreFile.replace('.csv','')+"'"+"," + "'"+str(row_id[0])+"'"+",'"+nombreFile.replace('.csv','')+"','"+ \
                        str(datetime.datetime.now())+"');"
                cur.execute(sqlquerys)
                conn.commit()

                cur.close()
                conn.close()
                return jsonify({"state": "Successfull"})
            else:
                cur.close()
                conn.close()
                return jsonify({"Value": "exist"})
        else:
            raise Exception
    except Exception as e:
        print(e)
        return jsonify({"state": "Failed"})

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
        sqlquery = "select usuario.id, usuario.nombre, usuario.password , usuario.correo from usuario where usuario.password="+"'"+passwords+"'"+ "AND usuario.correo="+"'"+correos+"'"+ ";"
        cur.execute(sqlquery)
        rows = cur.fetchone()

        return jsonify({"state": "Successful", "nombre": rows[1], "correo":rows[3], "id": rows[0]})
        
    except Exception as e:
        print(e)
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

@app.route("/get-json/<json_id>")
def get_json(json_id):

    filename = f"{json_id}.json"

    try:
        data=open("./historic/"+filename,"r")
        enc=data.read()
        return enc
    except Exception as e:
        print(e)
        return jsonify({"state": "failed"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5002, debug=True)
    app.secret_key = os.urandom(24)