# main.py

import asyncio
import importlib
import os 
from pyrogram import Client, idle # <--- Client यहां इंपोर्टेड है
from pytgcalls import PyTgCalls
from pytgcalls.exceptions import NoActiveGroupCall

from config import API_ID, API_HASH, BOT_TOKEN, SESSION_NAME, LOG_CHANNEL_ID
from database.connect import init_db 

# हमने सादगी के लिए ALL_MODULES लिस्ट यहाँ परिभाषित की है
ALL_MODULES = ['start', 'help', 'welcome', 'leave', 'admin', 'player', 'controls']

# --- Client Initialization (जैसा कि आपने अंतिम कोड में किया था) ---
print("⚙️ Initializing Pyrogram Client...")
app = Client(
    SESSION_NAME,
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)
print("✅ Pyrogram Client initialized.")

print("⚙️ Initializing PyTgCalls Client...")
vc_client = PyTgCalls(app) 
print("✅ PyTgCalls Client initialized.")

# --- Helper for Logging (Simplified) ---
def LOGGER(name):
    def log_print(message):
        print(f"[{name}] {message}")
    return log_print

# --- Custom Initialization Logic ---
async def init():
    
    # 1. Database and Startup Checks
    await init_db() 
    
    # 2. Start Clients
    await app.start()
    
    # 3. Module Loading (Loads handlers)
    # यह वह सेक्शन है जो NameError पैदा कर रहा है
    for module_name in ALL_MODULES:
        try:
            # Try loading handlers/ module first
            importlib.import_module(f"handlers.{module_name}")
        except ModuleNotFoundError:
            try:
                # Then try music/ module
                importlib.import_module(f"music.{module_name}")
            except ModuleNotFoundError:
                LOGGER("XMUSIC.plugins").error(f"Module {module_name} not found.")

    LOGGER("XMUSIC.plugins").info("ᴍᴏᴅᴜʟᴇs ʟᴏᴀᴅᴇᴅ...")
    
    await vc_client.start()

    # 4. VC Check (Simplified) - Using LOG_CHANNEL_ID for the test
    try:
        await vc_client.stream_call(
            LOG_CHANNEL_ID,
            "http://docs.evostream.com/sample_content/assets/sintel1m720p.mp4"
        )
        await vc_client.leave_group_call(LOG_CHANNEL_ID) 
        
    except NoActiveGroupCall:
        LOGGER("XMUSIC").error(
            "ᴘʟᴇᴀsᴇ ᴛᴜʀɴ ᴏɴ ᴛʜᴇ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ᴏғ ʏᴏᴜʀ ʟᴏɢ ɢʀᴏᴜᴘ/ᴄʜᴀɴɴᴇʟ.\n\nɪɴғɪɴɪᴛʏᴇʀᴀ ʙᴏᴛ sᴛᴏᴘᴘᴇᴅ..."
        )
        exit()
    except Exception as e:
        LOGGER("XMUSIC").warning(f"Initial VC stream check failed (non-fatal): {e}")

    
    LOGGER("XMUSIC").info("ᴍᴜsɪᴄ ʀᴏʙᴏᴛ sᴛᴀʀᴛᴇᴅ sᴜᴄᴄᴇsғᴜʟʟʏ...")
    
    # 5. Idle and Stop
    await idle()
    await app.stop()
    await vc_client.stop()
    
    LOGGER("XMUSIC").info("sᴛᴏᴘᴘɪɴɢ ᴍᴜsɪᴄ ʙᴏᴛ ...")


if __name__ == "__main__":
    try:
        asyncio.get_event_loop().run_until_complete(init())
    except KeyboardInterrupt:
        LOGGER("XMUSIC").info("User requested shutdown (Ctrl+C).")
        if os.path.exists("downloads"):
             import shutil
             shutil.rmtree("downloads")
                                 
