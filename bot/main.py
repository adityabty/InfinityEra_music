# main.py

import asyncio
# ❗ यह लाइन 'Client' एरर को ठीक करती है
from pyrogram import Client
from pytgcalls import PyTgCalls
from config import API_ID, API_HASH, BOT_TOKEN, SESSION_NAME, LOG_CHANNEL_ID
from database.connect import init_db

# --- 1. Pyrogram Client Initialization ---
print("⚙️ Initializing Pyrogram Client...")
app = Client(
    SESSION_NAME,  # 'InfinityEraMusic'
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    # यह 'handlers' फ़ोल्डर से सभी इवेंट हैंडलर्स (commands, welcome, play) को लोड करता है
    plugins=dict(root="handlers")  
)
print("✅ Pyrogram Client initialized.")

# --- 2. PyTgCalls Client Initialization (VC Music) ---
# PyTgCalls client Pyrogram client (app) का उपयोग करता है
print("⚙️ Initializing PyTgCalls Client...")
vc_client = PyTgCalls(app)
print("✅ PyTgCalls Client initialized.")


async def main():
    
    # --- 3. Database Connection ---
    # MongoDB Atlas से कनेक्ट होता है
    await init_db() 
    
    # --- 4. Start Clients ---
    print("\n🚀 Starting InfinityEra Bot (Pyrogram & PyTgCalls)...")
    try:
        # Pyrogram Bot Client शुरू करें
        await app.start()
        print("✅ Pyrogram App Started.")
        
        # PyTgCalls Voice Chat Client शुरू करें
        await vc_client.start()
        print("✅ PyTgCalls VC Client Started.")
        
        # --- 5. Final Status Print ---
        me = await app.get_me()
        print("-" * 40)
        print(f"🤖 Bot Started Successfully!")
        print(f"Name: {me.first_name}")
        print(f"Username: @{me.username}")
        print(f"ID: {me.id}")
        print("-" * 40)
        
        # Log Channel को स्टार्टअप नोटिफिकेशन भेजें
        try:
            await app.send_message(LOG_CHANNEL_ID, "✨ **InfinityEra Bot** is online and running!")
        except Exception:
            pass
        
        # --- 6. Keep Running ---
        # बॉट को निरंतर चालू रखने के लिए
        await asyncio.Future() 

    except Exception as e:
        print(f"\n❌ FATAL ERROR during startup: {e}")
        # यह FATAL ERROR आमतौर पर गलत TOKEN/API_ID/API_HASH के कारण होता है
        print("Please check your API_ID, API_HASH, and BOT_TOKEN in config.py / .env.")
    finally:
        # अगर कोई FATAL ERROR होती है, तो क्लाइंट्स को शालीनता से बंद करें
        await app.stop()
        await vc_client.stop()
        print("\n😴 Bot stopped.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nUser requested shutdown (Ctrl+C). Exiting...")

