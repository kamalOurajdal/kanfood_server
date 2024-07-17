from pymongo import MongoClient
from django.conf import settings

client = MongoClient("mongodb://localhost:27017/")
db = client["recipe_db"]