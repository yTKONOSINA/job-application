from pymongo import MongoClient 

client = MongoClient('localhost', 27017)
db = client['test_database']
users_collection = db['users_collection']