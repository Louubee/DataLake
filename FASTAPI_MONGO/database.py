import os
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")


client = MongoClient(MONGO_URI, server_api=ServerApi('1'))

db = client["DataLake_Clean"]

# Collections
social_collection = db["social_media_clean"]
transactions_collection = db["transactions_clean"]
logs_collection = db["logs_clean"]
users_collection = db["users_collection"]
usage_collection = db["api_usage"]

