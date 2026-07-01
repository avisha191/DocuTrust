import os

from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(
    os.getenv("MONGO_URI")      # Change to MONGODB_URI if that's your variable name
)

db = client["DocuTrust"]

interaction_logs = db["interaction_logs"]