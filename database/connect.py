from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URL, DB_NAME

# Global database client
mongo_client = AsyncIOMotorClient(MONGO_URL)
database = mongo_client[DB_NAME]

async def init_db():
    print("Connecting to MongoDB...")
    try:
        # Check connection
        await mongo_client.server_info()
        print(f"Successfully connected to MongoDB | Database: {DB_NAME}")
    except Exception as e:
        print(f"ERROR: Could not connect to MongoDB. {e}")
        # Exit or handle error appropriately
        exit()

# Collections
USERS_COL = database.users
GROUPS_COL = database.groups
LOGS_COL = database.logs
SONGS_COL = database.songs
