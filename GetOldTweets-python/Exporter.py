# -*- coding: utf-8 -*-
#Repositorio de extraccion de tweets creado por Jefferson-Enrique, fuente: https://github.com/Jefferson-Henrique/GetOldTweets-python
#Importamos las siguientes librerias:
#Unidecode: Eliminar caracteres con tildes o ñ
#codecs: usado para guardar en el csv
#classifier: usada para la prediccion de sentimientos de los tweets. Repositorio creado por aylliote, fuente: https://github.com/aylliote/senti-py
import sys,getopt,datetime,codecs, unidecode, csv, requests, re
import pandas as pd
from classifier import *
from textblob import TextBlob
from langdetect import detect, DetectorFactory
if sys.version_info[0] < 3:
    import got
else:
    import got3 as got

global outputFileName
outputFileName=''
global h
h=0
DetectorFactory.seed=0
def main(argv):

	if len(argv) == 0:
#Los parametros se especifican mas adelante en la linea 28
		print('You must pass some parameters. Use \"-h\" to help.')
		return

	if len(argv) == 1 and argv[0] == '-h':
#Ayuda para los comandos y el programa en general
		f = open('exporter_help_text.txt', 'r')
		print (f.read())
		f.close()

		return

	try:
		opts, args = getopt.getopt(argv, "",(	"querysearch=", "exact=", "username=", "any=", "exclude=", "hashtag=", "author=",
												"recipient=", "mention=", "near=", "within=", "since=", "until=",
												"lang=", "maxtweets=", "toptweets", "output=")
											)

		tweetCriteria = got.manager.TweetCriteria()
		outputFileName = ''
		name1=''
		name2=''
		name3=''
		for opt,arg in opts:
#Buscar por usuario
			if opt == '--username':
				tweetCriteria.username = arg
				name3 = arg.replace(" ","")
#Buscar desde una fecha especifica
			elif opt == '--since':
				tweetCriteria.since = arg
#Buscar hasta una fecha especifica
			elif opt == '--until':
				tweetCriteria.until = arg
#Buscar por una palabra clave o hashtags
			elif opt == '--querysearch':
				tweetCriteria.querySearch = " "+arg
				name1 = arg.replace(" ","")
#Buscar solo los tweets mas revelantes, no se requiere ingresar algun parametro extra
			elif opt == '--toptweets':
				tweetCriteria.topTweets = True
#Buscar hasta un maximo de tweets
			elif opt == '--maxtweets':
				tweetCriteria.maxTweets = int(500)

			elif opt == '--exact':
				tweetCriteria.exactSearch = arg

			elif opt == '--any':
				tweetCriteria.anySearch = arg

			elif opt == '--exclude':
				tweetCriteria.excludeSearch = arg

			elif opt == '--hashtag':
				tweetCriteria.hashtag = arg
				name2=arg.replace(" ","")

			elif opt == '--author':
				tweetCriteria.author = arg

			elif opt == '--recipient':
				tweetCriteria.recipient = arg

			elif opt == '--mention':
				tweetCriteria.mention = arg			

			elif opt == '--near':
				tweetCriteria.location = arg

			elif opt == '--within':
				tweetCriteria.radius = int(arg)
#Archivo por defecto en donde se guardaran los resultados
			elif opt == '--lang':
				tweetCriteria.lang = arg

			elif opt == '--output':
				outputFileName = arg
			if(name1 is not ''):
				if(name2 is not ''):
					outputFileName = str(name1.replace(" ","") + name2.replace(" ","")+".csv")
				else:
					outputFileName = str(name1.replace(" ","")+".csv")
			elif(name1 is ''):
				if(name2 is not ''):
					outputFileName = str(name2.replace(" ","")+".csv")
				else:
					if(name3 is not ''):
						outputFileName = str(name3.replace(" ","")+".csv")
			outputFile = codecs.open(outputFileName, "w+", "utf-8")
#Encabezado para el csv
			outputFile.write('username;date;0;00;text;geo;mentions;hashtags;id;permalink;sentimiento;rango')
		print('Searching...\n')


		def receiveBuffer(tweets):
#Se crean arreglos para poder procesar los tweets por bloques
			textos=[]
			sentimientos=[]
			usuarios=[]
			fechas=[]
			favoritos=[]
			rts=[]
			geos=[]
			menciones=[]
			hashtags=[]
			ids=[]
			links=[]
			popularidadR=[]
#Se inicia el clasificador de sentimientos
			clf = SentimentClassifier()
			for t in tweets:
				texto = re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', '', t.text.replace(';',','), flags=re.MULTILINE)
				texto = re.sub(r'(pic.twitter)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', '', t.text.replace(';',','), flags=re.MULTILINE)
				if(texto is not ""):
					textos.append(unidecode.unidecode(texto.replace('-',' ')))
					usuarios.append(unidecode.unidecode(t.username))
					fechas.append(t.date.strftime("%Y-%m-%d %H:%M"))
					favoritos.append(t.favorites)
					menciones.append(t.mentions)
					hashtags.append(unidecode.unidecode(t.hashtags))
					ids.append(t.id)
					geos.append(t.geo)
					links.append(t.permalink)
					rts.append(t.retweets)
					global h
					h=h+1
				else:
					h=h-1
				if(h<500):
					if(len(textos)>=1):
	#Cada 100 tweets se ejecuta el clasificador y se guarda en el csv
						for tex in textos:
							popular=''
							try:
								lang=detect((tex.replace('#','')).replace('@',''))
							except:
								lang='es'
							if(lang=='es'):
								popularidad = clf.predict((tex.replace('#','')).replace('@',''))
								popularidadR.append(popularidad)
								if(popularidad<0.5):
									if(popularidad<0.3):
										popular="Muy negativo"
									else:
										popular="Tendencia negativa"
								else:
									if(popularidad>0.7):
										popular="Muy positivo"
									else:
										popular="Tendencia positiva"
								sentimientos.append(popular)
							else:
								popularidad=TextBlob((tex.replace('#','')).replace('@',''))
								popularidadR.append(popularidad.sentiment.polarity)
								if(popularidad.sentiment.polarity<(0)):
									if(popularidad.sentiment.polarity<(-0.6)):
										popular="Muy negativo"
									else:
										popular="Tendencia negativa"
									sentimientos.append(popular)
								else: 
									if(popularidad.sentiment.polarity>0):
										if(popularidad.sentiment.polarity>0.7):
											popular="Muy positivo"
											sentimientos.append(popular)
										else:
											popular="Tendencia positiva"
											sentimientos.append(popular)
								if(popularidad.sentiment.polarity==0):
									popular="Neutral"
									sentimientos.append(popular)
						for i in range(len(textos)):
							outputFile.write(('\n%s;%s;%d;%d;"%s";%s;%s;%s;"%s";%s;%s;%s' % (usuarios[i], fechas[i], rts[i], favoritos[i], textos[i], geos[i], menciones[i], hashtags[i], ids[i], links[i], sentimientos[i], popularidadR[i])))
						textos=[]
						sentimientos=[]
						usuarios=[]
						fechas=[]
						favoritos=[]
						rts=[]
						geos=[]
						menciones=[]
						hashtags=[]
						ids=[]
						links=[]
						popularidadR=[]
				else:
					outputFile.flush()
					raise ValueError()
					break
			print(h)
			print('More %d saved on file...\n' % len(tweets))
		if(h<500):
			got.manager.TweetManager.getTweets(tweetCriteria, receiveBuffer)
		else:
			raise Exception

	except arg:
		print('Arguments parser error, try -h' + arg)
		return 1
	finally:
		outputFile.close()
		print('Done. Output file generated "%s".' % outputFileName)

if __name__ == '__main__':
	main(sys.argv[1:])
