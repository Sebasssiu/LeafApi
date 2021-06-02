import pymongo


class MongoInstance:
    def __init__(self):
        client = pymongo.MongoClient(
            "mongodb+srv://sebas:sebas@leafapi.l5vod.mongodb.net/leafApi?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE&retryWrites=true&w=majority", connect=False)
        self.db = client.leafApi
