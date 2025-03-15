from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

CONNECTION_STRING = os.getenv("MONGO_CONNECTION_STRING")
DATABASE_NAME = os.getenv("MONGO_DB_NAME")


def get_database():
    client = MongoClient(CONNECTION_STRING)

    db = client[DATABASE_NAME]
    
    return db
