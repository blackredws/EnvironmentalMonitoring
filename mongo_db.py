from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

db = client["environmental_monitoring"]

humidity_collection = db["humidity_data"]