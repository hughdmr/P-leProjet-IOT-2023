# pip install pymongo
# pip install bson
import pymongo
from bson import ObjectId

# Connection avec la base de donnée que j'ai importée sur MongoDB Compass
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["IOT"]
mycol = mydb["IOT"]

# Obtenir toutes les infos du paquet nommé id : ...
myquery = {'_id': ObjectId('640f3c14f628ec64b0f70c65')}
mydoc = mycol.find(myquery)

# Obtenir les valeurs distinctes des taille_up
myquery2 = mycol.distinct('taille_up')

for x in myquery2:
    print(x)

# MongoDB Compass
# J'ai pas fait les trucs proprements mais j'ai un peu tout installé comme un bourrin MongoDB Compass, mongodb-atlas. Le mieux serait de suivre un tuto.
# Après faut upload le fichier csv sur MongoDB Compass
