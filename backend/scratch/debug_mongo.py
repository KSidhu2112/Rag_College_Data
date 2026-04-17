import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = "learnhub_db"
COLLECTION_NAME = "chat_history"

def debug_mongo():
    try:
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        col = db[COLLECTION_NAME]
        
        print(f"Total docs in {COLLECTION_NAME}: {col.count_documents({})}")
        
        distinct_sessions = col.distinct("SessionId")
        print(f"Distinct Sessions: {distinct_sessions}")
        
        # Look at one sample document
        sample = col.find_one()
        print(f"Sample Document: {sample}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug_mongo()
