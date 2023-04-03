# pip install pymongo
# pip install bson
import pymongo
import csv
import os
from bson import ObjectId

# Connection avec la base de donnée que j'ai importée sur MongoDB Compass
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["IOT"]
mycol = mydb["IOT"]


def query_mongo(myquery, mycol):
    ###Entrée1 : requête
    # Obtenir les infos d'un paquet : dictionnaire // Exemple : myquery = {'_id': ObjectId('640f3c14f628ec64b0f70c65')}
    # Obtenir une colonne : string // Exemple : 'taille_up'
    # Entrée2 : la base de données Mongo
    # Sortie : la réponse de la base de données

    # Obtenir toutes les infos d'un paquet
    if type(myquery) == 'dict':
        query = mycol.find(myquery)

    # Obtenir les valeurs distinctes des taille_up
    elif type(myquery) == 'str':
        query = mycol.distinct('taille_up')

    for x in query:
        print(x)


def importcsv_MongoCompass(csv_name, mycol):
    # Entrée :
    #csv_name : str
    # mycol : la base de données Mongo

    header = ['', 'Session', 'Taille_up', 'Taille_down', 'Taille', 'Delta', 'StartTime', 'EndTime', 'StartTime_sup', 'EndTime_sup',
              'StartTime_inf', 'EndTime_inf', 'Delta_sup', 'Delta_inf', 'Dongle_port', 'SensorId', 'NumberOfPackets', 'Info', 'sleep']

    csv_file = open(csv_name, 'r')
    reader = csv.DictReader(csv_file)
    for each in reader:
        row = {}
        for field in header:
            row[field] = each[field]
            # print(row[field])
        insert_row = mycol.insert_one(row)


if __name__ == '__main__':
    #query1 = {'_id': ObjectId('640f3c14f628ec64b0f70c65')}
    #query2 = 'taille_up'
    # print(f'The first query for the info of the Object {query1['_id']}')
    #query_mongo(query1, mycol)
    #print('The second query : get the taille up of all the Objects')
    #query_mongo(query2, mycol)

    directory = 'dfincsv'
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        if os.path.isfile(f):
            print(filename)
            newfilename = f'{directory}\{filename}'
            importcsv_MongoCompass(newfilename, mycol)

# MongoDB Compass
# J'ai pas fait les trucs proprements mais j'ai un peu tout installé comme un bourrin MongoDB Compass, mongodb-atlas. Le mieux serait de suivre un tuto.
# Après faut upload le fichier csv sur MongoDB Compass
