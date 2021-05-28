import pymongo


class MongoInstance:
    def __init__(self):
        self.client = pymongo.MongoClient(
            "mongodb+srv://sebas:sebas@leafapi.l5vod.mongodb.net/leafApi?retryWrites=true&w=majority")
        self.db = self.client['dev']

    def change_database(self, database):
        self.db = self.client[database]
