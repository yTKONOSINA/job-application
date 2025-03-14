from pymongo import MongoClient

class DataBase:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DataBase, cls).__new__(cls)
            # Set up the connection here instead of __init__
            cls._instance.client = MongoClient('localhost', 27017)
            cls._instance.db = cls._instance.client['test_database']
            cls._instance.users_collection = cls._instance.db['users_collection']
        return cls._instance

if __name__ == "__main__":
    db1 = DataBase()
    db2 = DataBase()

    print(db1 is db2)  # True (same instance)
    print(db1.users_collection is db2.users_collection)  # True (same collection)

