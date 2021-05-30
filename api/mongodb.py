import pymongo


class MongoInstance:
    def __init__(self):
        client = pymongo.MongoClient(
            "mongodb+srv://sebas:sebas@leafapi.l5vod.mongodb.net/leafApi?retryWrites=true&w=majority")
        self.db = client.leafApi
