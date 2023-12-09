import json
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['example']
collection = db['news']

with open('modified.json') as file:
    file_data = json.load(file)
    print(file_data)

# if pymongo >= 3.0 use insert_many() for inserting many documents
#collection.insert_many(file_data)

client.close()
