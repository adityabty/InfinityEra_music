
# config.py
import os

API_ID = int(os.environ.get("API_ID", "123456"))      # अपने API_ID डालो
API_HASH = os.environ.get("API_HASH", "your_api_hash")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "your_bot_token")

YT_API_KEY = os.environ.get("YT_API_KEY", "your_youtube_api_key")  # optional (we use search lib)
MONGO_URI = os.environ.get("MONGO_URI", "mongodb+srv://user:pass@cluster.mongodb.net/InfinityEra")

OWNER_ID = int(os.environ.get("OWNER_ID", "123456789"))
LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "-1001234567890"))  # dev log channel id

# temp dir for downloads
DOWNLOADS_DIR = os.environ.get("DOWNLOADS_DIR", "./downloads")
os.makedirs(DOWNLOADS_DIR, exist_ok=True)
