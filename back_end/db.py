from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["logdb"]
logs_collection = db["logs"]

logs_collection.insert_many([
{
  "time": "2025-06-03 15:00",
  "location": "Sector A",
  "battery": 78
}
])