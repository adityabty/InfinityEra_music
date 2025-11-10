# db.py
from pymongo import MongoClient
from datetime import datetime
from config import MONGO_URI

client = MongoClient(MONGO_URI)
db = client.get_database()  # default DB from URI

users_col = db.get_collection("users")
groups_col = db.get_collection("groups")
logs_col = db.get_collection("logs")
songs_col = db.get_collection("songs")

def log_event(event_type, chat_id=None, user_id=None, song_name=None, extra=None):
    doc = {
        "event_type": event_type,
        "chat_id": chat_id,
        "user_id": user_id,
        "song_name": song_name,
        "extra": extra or {},
        "timestamp": datetime.utcnow()
    }
    logs_col.insert_one(doc)
