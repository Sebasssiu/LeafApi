import pymongo


class MongoInstance:
    def __init__(self):
        self.client = pymongo.MongoClient(
            "mongodb+srv://sebas:sebas@leafapi.l5vod.mongodb.net/leafApi?retryWrites=true&w=majority")
        self.db = self.client['dev']
        self.collection = self.db['test']

    def change_database(self, database):
        self.db = self.client[database]

    def change_collection(self, collection):
        self.collection = self.db[collection]