# main.py

import asyncio
import importlib
import os 
from pyrogram import Client, idle
from pytgcalls import PyTgCalls
from pytgcalls.exceptions import NoActiveGroupCall

from config import API_ID, API_HASH, BOT_TOKEN, SESSION_NAME, LOG_CHANNEL_ID
from database.connect import init_db 
# Assumption: You have a list of all module filenames (e.g., ['start', 'play', 'admin'])
# We will create a simple ALL_MODULES list here for demonstration:
ALL_MODULES = ['start', 'help', 'welcome', 'leave', 'admin', 'player', 'controls']

# --- Client Initialization (as defined previously) ---
print("⚙️ Initializing Pyrogram Client...")
app = Client(
    SESSION_NAME,
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)
print("✅ Pyrogram Client initialized.")

print("⚙️ Initializing PyTgCalls Client...")
# vc_client is your JARVIS equivalent for VC handling
vc_client = PyTgCalls(app) 
print("✅ PyTgCalls Client initialized.")

# --- Helper for Logging (Simplified) ---
def LOGGER(name):
    # In a simple setup, we just use print, but you can integrate your database/logs.py here
    def log_print(message):
        print(f"[{name}] {message}")
    return log_print

# --- Custom Initialization Logic ---
async def init():
    
    # 1. Database and Startup Checks
    await init_db() 
    
    # Note: Your InfinityEra bot does not use STRING sessions, 
    # so the session check is not needed here.
    
    # Note: Your InfinityEra bot does not currently implement
    # global banning or sudo checks in the startup file.
    
    # 2. Start Clients
    await app.start()
    
    # 3. Module Loading (Loads handlers from the 'handlers' and 'music' folders)
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

    # Note: userbot is not used in your simpler setup, so we skip userbot.start()
    
    await vc_client.start()

    # 4. VC Check (Simplified) - Using a dummy stream test
    try:
        # NOTE: Since this bot runs on the main client 'app', 
        # it must join a group chat where it has been added and VC is on.
        # We need a LOG_GROUP_ID for this check, assuming LOG_CHANNEL_ID is a Group/Channel ID
        await vc_client.stream_call(
            LOG_CHANNEL_ID, # Use your log channel/group ID for the test
            "http://docs.evostream.com/sample_content/assets/sintel1m720p.mp4"
        )
        # Immediately stop the stream after connecting successfully
        await vc_client.leave_group_call(LOG_CHANNEL_ID) 
        
    except NoActiveGroupCall:
        LOGGER("XMUSIC").error(
            "ᴘʟᴇᴀsᴇ ᴛᴜʀɴ ᴏɴ ᴛʜᴇ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ᴏғ ʏᴏᴜʀ ʟᴏɢ ɢʀᴏᴜᴘ/ᴄʜᴀɴɴᴇʟ.\n\nɪɴғɪɴɪᴛʏᴇʀᴀ ʙᴏᴛ sᴛᴏᴘᴘᴇᴅ..."
        )
        exit()
    except Exception as e:
        # General error during stream check (e.g., bot not admin in log channel VC)
        LOGGER("XMUSIC").warning(f"Initial VC stream check failed (non-fatal): {e}")


    # Note: vc_client.decorators() is skipped unless you implement it in your framework
    
    LOGGER("XMUSIC").info("ᴍᴜsɪᴄ ʀᴏʙᴏᴛ sᴛᴀʀᴛᴇᴅ sᴜᴄᴄᴇsғᴜʟʟʏ...")
    
    # 5. Idle and Stop
    await idle()
    await app.stop()
    await vc_client.stop()
    
    LOGGER("XMUSIC").info("sᴛᴏᴘᴘɪɴɢ ᴍᴜsɪᴄ ʙᴏᴛ ...")


if __name__ == "__main__":
    # Ensure correct event loop handling
    try:
        asyncio.get_event_loop().run_until_complete(init())
    except KeyboardInterrupt:
        LOGGER("XMUSIC").info("User requested shutdown (Ctrl+C).")
        # Clean up files in the downloads folder before exit
        if os.path.exists("downloads"):
             import shutil
             shutil.rmtree("downloads")
    
