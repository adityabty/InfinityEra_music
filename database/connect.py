# database/connect.py

from motor.motor_asyncio import AsyncIOMotorClient

# ⚠️ F I X: MONGO_URL को सीधे यहां सेट करें ताकि .env लोडिंग की समस्या ठीक हो जाए
# यह वह Atlas URI है जिसे आपने प्रदान किया है:
MONGO_URL = "mongodb+srv://rj5706603:O95nvJYxapyDHfkw@cluster0.fzmckei.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# डेटाबेस का नाम सेट करें
DB_NAME = "InfinityEraDB"

# Global database client
mongo_client = AsyncIOMotorClient(MONGO_URL)
database = mongo_client[DB_NAME]

async def init_db():
    print("Connecting to MongoDB...")
    try:
        # Check connection
        await mongo_client.server_info()
        print(f"✅ Successfully connected to MongoDB | Database: {DB_NAME}")
    except Exception as e:
        print(f"❌ ERROR: Could not connect to MongoDB. Connection details: {e}")
        # Re-raise the exception to stop bot execution if database connection fails
        raise ConnectionError(f"Database connection failed. Check Network Access and URI. Error: {e}")

# Collections
USERS_COL = database.users
GROUPS_COL = database.groups
LOGS_COL = database.logs
SONGS_COL = database.songs
