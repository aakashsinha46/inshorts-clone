from pymongo import MongoClient
client = MongoClient('localhost',27017)
db = client['example']
country = db['country']
category = db['category']
news = db['news']

data = [{"title":"Australia"}, {"title":"Canada"}, {"title":"Malaysia"}, {"title":"Singapore"}]

#print(collection.insert_many(data))


client.close()
def chooseCategory(category:None):
    #country.find(where id is 1)
    # data = categores

    categoryName = int(input())
    
def chooseCountry():
    print('welcome choose country')
    print('1. Australia ')
    print('2. Canada ')
    print('3. Malaysia ')
    print('4. singapore ')
ty
    countryName = int(input()) # countryName = 1

    chooseCategory(countryName)

if __name__ == "__main__":
    chooseCountry()
