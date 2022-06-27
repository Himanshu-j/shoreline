"""
Initialise the MongoDB connection/client and create shoreline DB
"""
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
shoreline_db = client.shoreline
