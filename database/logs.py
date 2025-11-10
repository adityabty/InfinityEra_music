# database/logs.py

from database.connect import LOGS_COL
from config import LOG_CHANNEL_ID
from pyrogram import Client
from datetime import datetime

async def log_action_to_mongodb(
    event_type: str, 
    chat_id: int, 
    user_id: int, 
    details: str
):
    """Log an action to the MongoDB logs collection."""
    log_entry = {
        "event_type": event_type,  # e.g., "PLAY_SONG", "USER_JOIN", "LEAVE_VC"
        "chat_id": chat_id,
        "user_id": user_id,
        "details": details,       # e.g., song_name, username
        "timestamp": datetime.now().isoformat()
    }
    await LOGS_COL.insert_one(log_entry)

async def log_action_to_channel(
    client: Client, 
    chat_id: int, 
    user_id: int, 
    action: str, 
    song_name: str
):
    """Log an action to the Telegram log channel."""
    # Fetch chat and user info
    try:
        chat = await client.get_chat(chat_id)
        user = await client.get_users(user_id)
        
        log_message = (
            f"[**InfinityEra-LOG**]\n"
            f"**Chat:** `{chat.title}` (`{chat_id}`)\n"
            f"**User:** `{user.first_name}` (@{user.username or 'None'} | `{user_id}`)\n"
            f"**Action:** `{action}`\n"
            f"**Song:** `{song_name}`\n"
            f"**Time:** `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`"
        )
        
        await client.send_message(
            LOG_CHANNEL_ID, 
            log_message
        )
        await log_action_to_mongodb(action, chat_id, user_id, song_name)
        
    except Exception as e:
        print(f"Error logging to channel/DB: {e}")
      
