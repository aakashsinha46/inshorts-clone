import pprint
from pymongo import MongoClient
import json
from bson.objectid import ObjectId


#database Connection at localhost:27017
client = MongoClient('localhost',27017)

#database Collections
db = client['example']
countryDB = db['country']
categoryDB = db['category']
newsDB = db['news']
#data list
countryList = ["Australia","Canada","Malaysia","Singapore"]
categoryList = ['politics', 'business', 'world', 'sports', 'lifestyle', 'technology', 'health', 'entertainment', 'fashion']

def countryAdder():
   countryIdCounter = 1
   for key,countryName in enumerate(countryList):
      countryIdCounter = key + 1
      countryDB.insert_one({'_id': countryIdCounter, "title": countryName})

def countryToCategoryMapp():
   countryIdCounter = 1
   inner = {}
   innerlist=[]
   categoryQuery = {}
   for key,countryName in enumerate(countryList):
      countryIdCounter = key + 1
      for categoryName in categoryList:
         id = categoryDB.insert_one({"title": categoryName}).inserted_id  
         inner['name'] = categoryName
         inner['refId'] = id 
         innerlist.append(inner.copy()) # .copy() method is used to remove repeating cause normal copy repeats
      categoryQuery['category'] = innerlist
      
      #mapping by inserting categoryid to conutry collection
      countryDB.update_many({"_id": countryIdCounter}, {"$set":categoryQuery},upsert=True)
      
      #clear the list and dict
      innerlist.clear()
      categoryQuery.clear()

def categoryToNewsMapp(jsonFileDir):
   innerlist = []
   newsQuery = {}
   #id is going to depend upon routing of dir 

   for keys, values in jsonFileDir.items():
      country = list(countryDB.find({'_id':keys}))
      for jsonItem in values:
         with open(jsonItem) as file:
            file_data = json.load(file)
            for key, value in file_data.items():
               for item in country[0]['category']:
                  if item['name'] == key:
                     refId = (item['refId'])
                     for news in value:
                        newsId = newsDB.insert_one(news).inserted_id
                        innerlist.append(newsId)
               newsQuery['newsId']= innerlist
               categoryDB.update_one({"_id": refId}, {"$set":newsQuery},upsert=True)
               newsQuery.clear() 
               innerlist.clear()
   
   #pprint.pprint(jsonFileDir)
   #pprint.pprint(categoryDB.find({'_id':refId}))
   '''
   with open('tage.json') as file:
      file_data = json.load(file)
      for item in file_data['politics']:
         #pprint.pprint(item)
         newsId = newsDB.insert_one(item).inserted_id
         #print(newsId)  
         innerlist.append(newsId)
      pprint.pprint(innerlist)
      newsQuery['newsId']= innerlist
      categoryDB.update_one({"_id": refId}, {"$set":newsQuery},upsert=True)
      #categoryDB.find({'_id': refId}).update(innerlist)
      newsQuery.clear() 
      innerlist.clear()

   #print(category)
   c = countryDB.find({"_id":1})
   print(c)
   for x in c:
      for y in x['category']:
         print(y['name'])
   '''
   
if __name__ == "__main__":
   countryAdder()
   countryToCategoryMapp()
   #categoryToNewsMapp()
   client.close()
