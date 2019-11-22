import os
import datetime, time, json, csv, jsonify, subprocess
from collections import Counter

def buscarTweets(busqueda='',hashtag='',usuario='', fecha_min='', cerca=''):
    #Se busca el script de busqueda de tweets
    path_script = os.path.abspath("Exporter.py")
    #Se castean y adaptan las variables para la busqueda
    fecha=datetime.datetime.now()
    year=fecha.year
    month=fecha.month
    day=fecha.day
    hashtag=hashtag.replace("#","").replace(" ","")
    filename=''
    if(fecha_min==''):
        f1=""+str(year-1)+"-"+str(month)+"-"+str(day)
    else:
        f1=fecha_min.replace('/','-')
    if(cerca==''):
        cercania='Colombia'
    else:
        cercania=cerca
    if(busqueda is not ''):
        if(hashtag is not ''):
            #Se envian los comandos de busqueda via terminal, vease el archivo exporter_help_text.txt
            filename=busqueda.replace(" ","")+hashtag.replace("#","").replace(" ","")
            busqueda=busqueda.replace(" ","")+" "+hashtag.replace("#","").replace(" ","")
            os.system("python3 "+path_script+" --querysearch '"+busqueda+"' --since "+str(f1)+" --near "+cercania)
        elif(hashtag is ''):
            filename=busqueda.replace(" ","")
            os.system("python3 "+path_script+" --querysearch '"+busqueda+"' --since "+str(f1)+" --near "+cercania)
    elif(busqueda is ''):
        if(hashtag is not ''):
            filename=hashtag.replace(' ','').replace("#","")
            os.system("python3 "+path_script+" --querysearch '"+hashtag+"'"+" --since "+str(f1)+" --near "+cercania)
        elif(hashtag is ''):
            if(usuario is not ''):
                filename=usuario.replace(' ','').replace('@','')
                os.system("python3 "+path_script+" --username '"+usuario.replace('@','')+"'"+" --since "+str(f1)+" --near "+cercania)
            else:
                os.system("python3 "+path_script+" --since "+str(f1))
    #Devuelve el nombre del archivo para realizar los analisis en el metodo datosGrafica()
    return filename

def datosGrafica(filename='output_got', length=0):
    try:
        #Se leen todos los tweets conseguidos dentro de su csv de salida
        archivo=''
        if('.csv' in ("./csv/"+filename)):
            archivo="./csv/"+filename
        else:
            archivo="./csv/"+filename+'.csv'
        #Se crean arreglos para los sentimientos, los rt, los fv, las menciones y los hashtags
        valoraciones=[]
        retweets=[]
        favoritos=[]
        hashtags=[]
        menciones=[]
        textos=[]
        with open(archivo,"rt") as csv_file:
            reader=csv.reader(csv_file, delimiter=';',skipinitialspace=True)
            for line in reader:
                try:
                    #Se guardan todas los resultados del csv en sus respectivos arreglos
                    valoraciones.append(line[10])
                    retweets.append(int(line[2]))
                    favoritos.append(int(line[3]))
                    hashtags.append(line[7])
                    menciones.append(line[6])
                    textos.append(line[4])
                except:
                    continue
        #Se declaran variables para poder devolver el json mas adelante
        muy_positivo=0
        muy_negativo=0
        tendencia_n=0
        tendencia_p=0
        mayor_rt=max(retweets)
        promedio_rt= sum(retweets) / len(retweets)
        mayor_fv=max(favoritos)
        promedio_fv= sum(favoritos) / len(favoritos)
        texto_rt=textos[retweets.index(mayor_rt)]
        texto_fv=textos[favoritos.index(mayor_fv)]
        rt_positivos=[]
        rt_tend_pos=[]
        rt_tend_neg=[]
        rt_negativos=[]
        fv_positivos=[]
        fv_tend_pos=[]
        fv_tend_neg=[]
        fv_negativos=[]
        p=0
        for i in valoraciones:
        #Se agrupa la cantidad de tweets de acuerdo a cada sentimiento
            try:
                if("Muy positivo" in i):
                    muy_positivo=muy_positivo+1
                    rt_positivos.append(retweets[p])
                    fv_positivos.append(favoritos[p])
                elif("Muy negativo" in i):
                    muy_negativo=muy_negativo+1
                    rt_negativos.append(retweets[p])
                    fv_negativos.append(favoritos[p])
                elif("Tendencia positiva" in i):
                    tendencia_p=tendencia_p+1
                    rt_tend_pos.append(retweets[p])
                    fv_tend_pos.append(favoritos[p])
                elif("Tendencia negativa" in i):
                    tendencia_n=tendencia_n+1
                    rt_tend_neg.append(retweets[p])
                    fv_tend_neg.append(favoritos[p])
            except:
                continue
            p += 1
        #Se extraen tanto las menciones como los hashtags mas populares, los primeros 4 de cada uno
        hpopulares=[word for word, word_count in Counter(hashtags).most_common(4)]
        mpopulares=[word for word, word_count in Counter(menciones).most_common(4)]
        #Se buscan los retweets y los favoritos de los tweets conseguidos y se agrupan por sentimiento
        if not rt_positivos:
            rt_positivos.append(0)
        if not rt_negativos:
            rt_negativos.append(0)
        if not rt_tend_pos:
            rt_tend_pos.append(0)
        if not rt_tend_neg:
            rt_tend_neg.append(0)
        if not fv_positivos:
            fv_positivos.append(0)
        if not fv_negativos:
            fv_negativos.append(0)
        if not fv_tend_pos:
            fv_tend_pos.append(0)
        if not fv_tend_neg:
            fv_tend_neg.append(0)
        #Se calculan los maximos rt y fv de los tweets por sentimiento
        maxRtPos=max(rt_positivos)
        maxRtNeg=max(rt_negativos)
        maxRtTPos=max(rt_tend_pos)
        maxRtTNeg=max(rt_tend_neg)
        maxFvPos=max(fv_positivos)
        maxFvNeg=max(fv_negativos)
        maxFvTPos=max(fv_tend_pos)
        maxFvTNeg=max(fv_tend_neg)
        #Los resultados obtenidos anteriormente se estructuran en un json que sera devuelto una vez el metodo finalice
        a={'Muy positivo':muy_positivo, 'Tendencia positiva':tendencia_p, 'Tendencia negativa':tendencia_n, 'Muy negativo':muy_negativo,
        'Maximo RT Muy positivo': maxRtPos,'Maximo Rt Tendencia Positiva': maxRtTPos, 'Maximo Rt Tendencia Negativa':maxRtTNeg, 
        'Maximo Rt Muy negativos': maxRtNeg,'Tweet mas Rt':texto_rt, 'Promedio RT': float(promedio_rt), 'Mayor Favorito Muy Positivo':maxFvPos, 
        'Mayor Favorito Tendencia positiva': maxFvTPos, 'Mayor Favorito Tendencia Negativa': maxFvTNeg, 'Mayor Favorito Muy Negativo': maxFvNeg,
        'Tweet mas Fv':texto_fv, 'Promedio Favorito':float(promedio_fv), 'Hashtags populares':hpopulares, 'Menciones populares':mpopulares,
        'Trama':length, 'Archivo':filename, 'Fecha':str(datetime.datetime.now())}
        resultado=json.dumps(a)
        print(resultado)
        return resultado
    except Exception as e:
        #En caso de encontrar algun error, se devolvera un json vacio al servidor
        print(e)
        a={'Muy positivo':0, 'Tendencia positiva':0, 'Tendencia negativa':0, 'Muy negativo':0,
        'Maximo RT Muy positivo': 0,'Maximo Rt Tendencia Positiva': 0, 'Maximo Rt Tendencia Negativa':0, 
        'Maximo Rt Muy negativos': 0,'Tweet mas Rt':'No encontrado', 'Promedio RT': 0, 'Mayor Favorito Muy Positivo':0, 
        'Mayor Favorito Tendencia positiva': 0, 'Mayor Favorito Tendencia Negativa': 0, 'Mayor Favorito Muy Negativo': 0,
        'Tweet mas Fv':'No encontrado', 'Promedio Favorito':0, 'Hashtags populares':[], 'Menciones populares':[],'Trama':length,
        'Archivo':filename}
        resultado=json.dumps(a)
        print(resultado)
        return resultado