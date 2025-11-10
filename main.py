from pyrogram import Client
from pytgcalls import PyTgCalls
from config import API_ID, API_HASH, BOT_TOKEN, SESSION_NAME
from database.connect import init_db
import asyncio

# Pyrogram Client
app = Client(
    "InfinityEraBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="handlers") # Handlers folder को plugins के रूप में लोड करें
)

# PyTgCalls Client (Voice Chat)
# NOTE: PyTgCalls को अक्सर एक user session की आवश्यकता होती है, bot token नहीं।
# यहाँ हम एक साधारण Client का उपयोग कर रहे हैं। यदि आपको user session की आवश्यकता है, 
# तो आपको एक separate userbot setup करना होगा।
vc_client = PyTgCalls(app, cache_duration=100)

async def main():
    await init_db()
    print("Starting bot...")
    
    # Start Pyrogram and PyTgCalls
    await app.start()
    await vc_client.start()
    
    # Bot info
    me = await app.get_me()
    print(f"Bot started as @{me.username} ({me.id})")
    
    # Keep the bot running
    await asyncio.Future()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped by user.")
        
