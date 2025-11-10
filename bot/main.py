import asyncio, os
from pyrogram import Client, filters, idle
from pytgcalls import PyTgCalls
from pytgcalls.types import AudioPiped
from pytgcalls.types.input_stream import InputAudioStream
from dotenv import load_dotenv
from .player import download_song, fetch_song

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
STRING_SESSION = os.getenv("STRING_SESSION")
LOG_CHANNEL_ID = int(os.getenv("LOG_CHANNEL_ID", "0"))

bot = Client("InfinityEraBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
user = Client("InfinityEraUser", api_id=API_ID, api_hash=API_HASH, session_string=STRING_SESSION)
call = PyTgCalls(user)


@bot.on_message(filters.command("start") & filters.private)
async def start_command(_, m):
    await m.reply_text(
        "🎵 **Welcome to InfinityEra Bot**\nSweet, Smart & Stylish Music for Your Telegram VC.\n\n✨ Powered by InfinityEra",
        quote=True
    )


@bot.on_message(filters.command("play") & filters.group)
async def play_song(_, m):
    if len(m.command) < 2:
        return await m.reply_text("Please provide a song name to play.")

    query = " ".join(m.command[1:])
    wait = await m.reply_text("⏳ Please wait while I fetch your song...")

    song_url, title = await fetch_song(query)
    if not song_url:
        return await wait.edit("❌ Failed to fetch song.")

    file_path = await download_song(song_url, title)
    await call.join_group_call(
        m.chat.id,
        AudioPiped(file_path, stream_type=InputAudioStream)
    )

    await wait.delete()
    await m.reply_photo(
        photo="https://i.ibb.co/G3GPRwM/music.jpg",
        caption=f"🎧 Now Playing: {title}\n🎤 Requested by: {m.from_user.mention}\n✨ Powered by InfinityEra"
    )


@bot.on_message(filters.command("stop") & filters.group)
async def stop_song(_, m):
    await call.leave_group_call(m.chat.id)
    await m.reply_text("🛑 Playback stopped.\n✨ Powered by InfinityEra")


async def main():
    await bot.start()
    await user.start()
    await call.start()
    print("✅ InfinityEra is live and ready!")
    await idle()

if __name__ == "__main__":
    asyncio.run(main())
