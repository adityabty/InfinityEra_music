# main.py

import asyncio
from pyrogram import Client
from pytgcalls import PyTgCalls
from config import API_ID, API_HASH, BOT_TOKEN, SESSION_NAME, LOG_CHANNEL_ID
from database.connect import init_db

# --- 1. Pyrogram Client Initialization ---
print("⚙️ Initializing Pyrogram Client...")
app = Client(
    SESSION_NAME,  # InfinityEraMusic
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="handlers")  # Handlers folder को plugins के रूप में लोड करें
)
print("✅ Pyrogram Client initialized.")

# --- 2. PyTgCalls Client Initialization (VC Music) ---
# PyTgCalls, Pyrogram client (app) का उपयोग करके Voice Chat फंक्शनालिटी को संभालता है।
print("⚙️ Initializing PyTgCalls Client...")
vc_client = PyTgCalls(app)
print("✅ PyTgCalls Client initialized.")


async def main():
    
    # main.py

# ... (other imports)
from database.connect import init_db # सुनिश्चित करें कि यह सही है
# ...

    
    # --- 4. Start Clients ---
    print("\n🚀 Starting InfinityEra Bot (Pyrogram & PyTgCalls)...")
    try:
        await app.start()
        print("✅ Pyrogram App Started.")
        
        await vc_client.start()
        print("✅ PyTgCalls VC Client Started.")
        
        # --- 5. Final Status Print ---
        me = await app.get_me()
        print("-" * 40)
        print(f"🤖 Bot Started Successfully!")
        print(f"Name: {me.first_name}")
        print(f"Username: @{me.username}")
        print(f"ID: {me.id}")
        print(f"Owner ID: {API_ID}")
        print("-" * 40)
        
        # Optional: Send startup notification to the log channel
        try:
            await app.send_message(LOG_CHANNEL_ID, "✨ **InfinityEra Bot** is online and running! (v2.0)")
        except Exception as e:
            print(f"Warning: Could not send startup message to log channel: {e}")
        
        # --- 6. Keep Running ---
        # बॉट को तब तक चालू रखें जब तक कि उसे रोका न जाए (जैसे Ctrl+C)
        await asyncio.Future() 

    except Exception as e:
        print(f"\n❌ FATAL ERROR during startup: {e}")
        print("Please check your API_ID, API_HASH, and BOT_TOKEN in config.py / .env.")
    finally:
        # Stop clients gracefully if an error occurs or loop exits
        await app.stop()
        await vc_client.stop()
        print("\n😴 Bot stopped.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nUser requested shutdown (Ctrl+C). Exiting...")

