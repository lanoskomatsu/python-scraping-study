from pymongo import MongoClient

def get_mongo():
    mongo_client = MongoClient('mongo', 27017)
    mongo_client['admin'].authenticate("root","example")
    return mongo_client