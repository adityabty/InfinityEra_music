import os
from dotenv import load_dotenv

# .env फ़ाइल से वेरिएबल्स लोड करें (सुरक्षा के लिए)
load_dotenv()

# Telegram Bot API
API_ID = int(os.getenv("API_ID", 123456))
API_HASH = os.getenv("API_HASH", "YOUR_API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID", 123456789))

# Voice Chat (PyTgCalls) Settings
SESSION_NAME = os.getenv("SESSION_NAME", "InfinityEraMusic") # Pyrogram session name

# MongoDB Settings
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DB_NAME = "InfinityEraDB"

# Developer Log Channel
LOG_CHANNEL_ID = int(os.getenv("LOG_CHANNEL_ID", -100123456789))

# Bot Info/Branding
SUPPORT_CHAT = "https://t.me/YourSupportChat"
UPDATE_CHANNEL = "https://t.me/YourUpdateChannel"
DEVELOPER_USER = "YourDeveloperUsername"
BRANDING_TEXT = "∞ InfinityEra"
