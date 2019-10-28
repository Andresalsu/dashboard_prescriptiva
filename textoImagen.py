# Importamos la libreria Pillow
from PIL import Image
from os import listdir
from os.path import isfile, join
import os
import csv
import unidecode, string
import base64
from pdf2image import convert_from_path
import shutil
# Importamos Pytesseract
import pytesseract, re

path = "/Users/andalval/Desktop/prueba datalicit/13. SECRETARIA DE EDUCACION DEL DISTRITO SED-LP-REDP-073-2019/"
archivos = [f for f in listdir(path) if isfile(join(path, f))]
i=1
for x in archivos:
    ruta = path + x
    try:
        os.stat(path+"/Imagenes para analizar")
    except:
        os.mkdir(path+"/Imagenes para analizar")
    rutanueva=path+"/Imagenes para analizar"
    if ruta.endswith('.pdf'):
        pages = convert_from_path(ruta, dpi=200)
        for page in pages:
            filename = x + "-" + str(i) + '.jpg'
            page.save(os.path.join(rutanueva,filename), 'JPEG')
            i=i+1
    else:
        print(x+" no es un PDF")
buscarPresupuesto(path)
#buscarCodigo(path)
#buscarObjeto(path)
#buscarPlazos(path)
#buscarFactoresEvaluacion(path)
shutil.rmtree(rutanueva, ignore_errors=True)

def buscarPresupuesto(path):
    pathb = path+"/Imagenes para analizar/"
    archivos = [f for f in listdir(path) if isfile(join(path, f))]
    palabra="presupuesto oficial"
    pytesseract.pytesseract.tesseract_cmd = r'/usr/local/Cellar/tesseract/4.1.0/bin/tesseract'
    # Abrimos la imagen
    for x in archivos:
        ruta = path + x
        if ruta.endswith('.jpg') and "PLIEGO" in x or "Pliego" in x:
            im = Image.open(ruta)
            # Utilizamos el método "image_to_string"
            # Le pasamos como argumento la imagen abierta con Pillow
            texto = pytesseract.image_to_string(im)
            texto=unidecode.unidecode(texto)
            datafile = ''
            with open("texto.txt", "w") as text_file:
                text_file.write(texto.encode().decode())
            with open("texto.txt", "r") as text_file:
                datafile = text_file.readlines()
            for i, line in enumerate(datafile):
                if palabra in line:
                    for l in datafile[i:i+5]:
                        l = l.translate(str.maketrans("","", string.punctuation))
                        comparacion=[int(s) for s in l.split() if s.isdigit()]
                        if not comparacion:
                            k=1
                        else:
                            print(comparacion)
            # Mostramos el resultado

def buscarCodigo(path):
    pathb = path+"/Imagenes para analizar/"
    archivos = [f for f in listdir(path) if isfile(join(path, f))]
    palabra="licitacion publica"
    pytesseract.pytesseract.tesseract_cmd = r'/usr/local/Cellar/tesseract/4.1.0/bin/tesseract'
    # Abrimos la imagen
    for x in archivos:
        ruta = path + x
        if ruta.endswith('.jpg') and "PLIEGO" in x or "Pliego" in x:
            im = Image.open(ruta)
            # Utilizamos el método "image_to_string"
            # Le pasamos como argumento la imagen abierta con Pillow
            texto = pytesseract.image_to_string(im)
            texto=unidecode.unidecode(texto)
            datafile = ''
            with open("texto.txt", "w") as text_file:
                text_file.write(texto.encode().decode())
            with open("texto.txt", "r") as text_file:
                datafile = text_file.readlines()
            for i, line in enumerate(datafile):
                if palabra in line:
                    for l in datafile[i:i+1]:
                        l = l.translate(str.maketrans("","", string.punctuation))
                        comparacion=[int(s) for s in l.split() if s.isdigit()]
                        if not comparacion:
                            k=1
                        else:
                            print(comparacion)
            # Mostramos el resultado

def buscarObjeto(path):
    pathb = path+"/Imagenes para analizar/"
    archivos = [f for f in listdir(path) if isfile(join(path, f))]
    palabra="objeto:"
    pytesseract.pytesseract.tesseract_cmd = r'/usr/local/Cellar/tesseract/4.1.0/bin/tesseract'
    # Abrimos la imagen
    for x in archivos:
        ruta = path + x
        if ruta.endswith('.jpg') and "PLIEGO" in x or "Pliego" in x:
            im = Image.open(ruta)
            # Utilizamos el método "image_to_string"
            # Le pasamos como argumento la imagen abierta con Pillow
            texto = pytesseract.image_to_string(im)
            texto=unidecode.unidecode(texto)
            datafile = ''
            with open("texto.txt", "w") as text_file:
                text_file.write(texto.encode().decode())
            with open("texto.txt", "r") as text_file:
                datafile = text_file.readlines()
            for i, line in enumerate(datafile):
                if palabra in line:
                    for l in datafile[i:i+7]:
                        l = l.translate(str.maketrans("","", string.punctuation))
                        comparacion=[int(s) for s in l.split() if s.isdigit()]
                        if not comparacion:
                            k=1
                        else:
                            print(comparacion)
            # Mostramos el resultado

def buscarPlazos(path):
    pathb = path+"/Imagenes para analizar/"
    archivos = [f for f in listdir(path) if isfile(join(path, f))]
    palabra="plazo de ejecución"
    pytesseract.pytesseract.tesseract_cmd = r'/usr/local/Cellar/tesseract/4.1.0/bin/tesseract'
    # Abrimos la imagen
    for x in archivos:
        ruta = path + x
        if ruta.endswith('.jpg') and "PLIEGO" in x or "Pliego" in x:
            im = Image.open(ruta)
            # Utilizamos el método "image_to_string"
            # Le pasamos como argumento la imagen abierta con Pillow
            texto = pytesseract.image_to_string(im)
            texto=unidecode.unidecode(texto)
            datafile = ''
            with open("texto.txt", "w") as text_file:
                text_file.write(texto.encode().decode())
            with open("texto.txt", "r") as text_file:
                datafile = text_file.readlines()
            for i, line in enumerate(datafile):
                if palabra in line:
                    for l in datafile[i:i+5]:
                        l = l.translate(str.maketrans("","", string.punctuation))
                        comparacion=[int(s) for s in l.split() if s.isdigit()]
                        if not comparacion:
                            k=1
                        else:
                            print(comparacion)
            # Mostramos el resultado

def buscarFactoresEvaluacion(path):
    pathb = path+"/Imagenes para analizar/"
    archivos = [f for f in listdir(path) if isfile(join(path, f))]
    palabra="factores de evaluacion"
    pytesseract.pytesseract.tesseract_cmd = r'/usr/local/Cellar/tesseract/4.1.0/bin/tesseract'
    # Abrimos la imagen
    for x in archivos:
        ruta = path + x
        if ruta.endswith('.jpg') and "PLIEGO" in x or "Pliego" in x:
            im = Image.open(ruta)
            # Utilizamos el método "image_to_string"
            # Le pasamos como argumento la imagen abierta con Pillow
            texto = pytesseract.image_to_string(im)
            texto=unidecode.unidecode(texto)
            datafile = ''
            with open("texto.txt", "w") as text_file:
                text_file.write(texto.encode().decode())
            with open("texto.txt", "r") as text_file:
                datafile = text_file.readlines()
            for i, line in enumerate(datafile):
                if palabra in line:
                    for l in datafile[i:i+9]:
                        l = l.translate(str.maketrans("","", string.punctuation))
                        comparacion=[int(s) for s in l.split() if s.isdigit()]
                        if not comparacion:
                            k=1
                        else:
                            print(comparacion)
            # Mostramos el resultado