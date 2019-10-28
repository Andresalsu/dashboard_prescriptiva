import csv
import unidecode
i=0
with open('entrenatweets.csv', mode='w') as csvfile:
    writeCSV = csv.writer(csvfile, delimiter=',')
    writeCSV.writerow(("target","ids","date","user","text","RT_Count","Favorite_Count"))
    with open('training.1600000.processed.noemoticon.csv') as csv_file:
        readCSV = csv.reader(csv_file, delimiter=',')
        for row in readCSV:
            writeCSV.writerow((row[0],row[1],unidecode.unidecode(row[2]),
            unidecode.unidecode(row[4]),unidecode.unidecode(row[5]),"0","0"))
            i=i+1
            print(i)