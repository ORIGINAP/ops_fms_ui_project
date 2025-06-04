from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["logdb"]
logs_collection = db["logs"]