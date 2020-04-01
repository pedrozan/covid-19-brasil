import urllib.parse

from pymongo import MongoClient


username = urllib.parse.quote_plus(os.environ['MONGO_USER'])
password = urllib.parse.quote_plus(os.environ['MONGO_PWD'])
conn = MongoClient(
    f"mongodb+srv://{username}:{password}@cluster0-rfxki.mongodb.net/test?retryWrites=true&w=majority"
)


def get_connection():
    db = conn.get_database("test")
    return db
