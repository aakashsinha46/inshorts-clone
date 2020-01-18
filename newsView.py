from pymongo import MongoClient
import pprint

#database Connection at localhost:27017
client = MongoClient('localhost',27017)

#database Collections
db = client['example']
countryDB = db['country']
categoryDB = db['category']
newsDB = db['news']

countryNames = {'australia':1,'canada':2,'malaysia':3,'singapore':4}
categoryList = {'politics':1, 'business':2, 'world':3, 'sports':4, 'lifestyle':5, 'technology':6, 'health':7, 'entertainment':8, 'fashion':9}

def chooseCategory(Id):
    print('choose a category')
    print(categoryList)
    
    catId = int(input())
    for key, value in categoryList.items():
        if catId == value:
            categoryName = key 

    data = list(countryDB.find({'_id':Id}))
    #print(data)
    
    for item in data[0]['category']:
        if item['name'] == categoryName:
            refId = item['refId']

    data = list(categoryDB.find({'_id':refId}))

    for item in data[0]["newsId"]:
        news = list(newsDB.find({'_id':item}))
        pprint.pprint(news)
        print('------------------------------------------------------------------')

    print('want more ......type 1 else 0')
    i = int(input())
    if i == 1:    
        chooseCountry()
    else:
        exit(1)

        
def chooseCountry():
    print("choose a country")
    print(countryNames)
    countryId = int(input())

    chooseCategory(countryId)

if __name__ == "__main__":
    chooseCountry()

