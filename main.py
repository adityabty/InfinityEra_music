# main.py
import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import API_ID, API_HASH, BOT_TOKEN, OWNER_ID, LOG_CHANNEL, DOWNLOADS_DIR
from utils import yt_search, download_audio, create_nowplaying_image
from db import log_event, users_col, groups_col, songs_col
from music_player import init_pytgcalls, play_track, pause, resume, stop, now_playing
from db import log_event
from pyrogram.types import Message

app = Client("InfinityEra", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
pytg = None

# Inline buttons template
def now_playing_kb():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("⏸ Pause", callback_data="pause"),
                InlineKeyboardButton("▶️ Resume", callback_data="resume"),
                InlineKeyboardButton("⏩ Skip", callback_data="skip"),
                InlineKeyboardButton("⏹ Stop", callback_data="stop")
            ],
            [
                InlineKeyboardButton("📢 Support", url="https://t.me/InfinityEraSupport"),
                InlineKeyboardButton("💬 Group", url="https://t.me/InfinityEraGroup"),
                InlineKeyboardButton("❌ Close", callback_data="close")
            ]
        ]
    )

@app.on_message(filters.command("start") & filters.private)
async def start_cmd(_, message: Message):
    await message.reply_text(
        "🎵 Welcome to InfinityEra Bot\nSweet, Smart & Stylish Music for Your Telegram VC.\n\n/ help to view commands",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("👨‍💻 Developer", url="https://t.me/your_dev")],
            [InlineKeyboardButton("➕ Add Me To Group", url=f"https://t.me/{(await _.get_me()).username}?startgroup=true")]
        ])
    )
    log_event("start", chat_id=message.chat.id, user_id=message.from_user.id, extra={"text": "/start"})

@app.on_message(filters.command("help"))
async def help_cmd(_, message):
    text = (
        "🎛️ InfinityEra Group Help Bot – Main Functions\n\n"
        "1️⃣ Moderation\n• Remove spam and links\n• Filter abusive words\n• Control message flooding\n\n"
        "2️⃣ User Management\n• Kick/Ban/Warn users\n• Auto warn-limit actions\n• Send welcome messages\n\n"
        "3️⃣ Security & Utilities\n• Captcha verification\n• /rules, /about\n• Protect group settings\n"
    )
    await message.reply_text(text, reply_markup=InlineKeyboardMarkup(
        [[InlineKeyboardButton("💬 Support", url="https://t.me/InfinityEraSupport"),
          InlineKeyboardButton("📢 Updates", url="https://t.me/InfinityEraUpdates"),
          InlineKeyboardButton("🧑‍💻 Developer", url="https://t.me/your_dev")]]
    ))

# Play command — group-only
@app.on_message(filters.command("play") & filters.group)
async def play_cmd(_, message):
    user = message.from_user
    chat_id = message.chat.id
    query = " ".join(message.command[1:])
    if not query:
        await message.reply_text("❗ Usage: /play <song name or youtube url>")
        return

    waiting = await message.reply_text("⏳ कृपया प्रतीक्षा करें…")  # auto-delete when playing starts

    # 1) search
    info = yt_search(query)
    if not info:
        await waiting.edit("❌ मिल नहीं पाया। दूसरा नाम try करो।")
        return

    title = info["title"]
    url = info["link"]
    thumb = info.get("thumbnail")

    # 2) download audio
    audio_path = await asyncio.get_event_loop().run_in_executor(None, download_audio, url, f"{chat_id}_%(title)s.%(ext)s")
    if not audio_path:
        await waiting.edit("❌ डाउनलोड में समस्या हुई।")
        return

    # 3) create now playing image
    now_img = os.path.join(DOWNLOADS_DIR, f"now_{chat_id}.jpg")
    try:
        create_nowplaying_image(thumb, title, f"[{user.first_name}](tg://user?id={user.id})", now_img)
    except Exception as e:
        # ignore image failure, proceed
        now_img = None

    # 4) play in VC
    try:
        await play_track(pytg, chat_id, audio_path, title, user)
    except Exception as e:
        await waiting.edit(f"❌ VC join/play error: {e}")
        return

    await waiting.delete()
    caption = f"🎧 Now Playing: {title}\n🎤 Requested by: [{user.first_name}](tg://user?id={user.id})\n✨ Powered by InfinityEra"
    if now_img and os.path.exists(now_img):
        await message.reply_photo(photo=now_img, caption=caption, reply_markup=now_playing_kb())
    else:
        await message.reply_text(caption, reply_markup=now_playing_kb())

    # log to DB + dev channel
    log_event("play", chat_id=chat_id, user_id=user.id, song_name=title)
    try:
        await app.send_message(LOG_CHANNEL,
            f"Chat: {message.chat.title} ({chat_id})\nUser: {user.mention} ({user.id})\nAction: play\nSong: {title}")
    except:
        pass

# Callback query handlers for inline buttons
@app.on_callback_query()
async def cb_handler(_, cq):
    data = cq.data
    chat = cq.message.chat
    chat_id = chat.id
    user = cq.from_user

    if data == "pause":
        try:
            await pause(chat_id, pytg)
            await cq.answer("⏸ Paused")
        except Exception as e:
            await cq.answer("Pause failed")
    elif data == "resume":
        try:
            await resume(chat_id, pytg)
            await cq.answer("▶️ Resumed")
        except:
            await cq.answer("Resume failed")
    elif data == "stop":
        try:
            await stop(chat_id, pytg)
            await cq.message.reply_text("⏹ Stopped playback and left VC.")
            await cq.answer()
        except:
            await cq.answer("Stop failed")
    elif data == "skip":
        # for starter: skip = stop. Advanced: maintain queue
        try:
            await stop(chat_id, pytg)
            await cq.message.reply_text("⏩ Skipped current track. Use /play to play next.")
            await cq.answer()
        except:
            await cq.answer("Skip failed")
    elif data == "close":
        try:
            await cq.message.delete()
            await cq.answer()
        except:
            await cq.answer()

# When bot joins voice chat event - greet (we'll send greeting on play)
# Group member join/leave welcome - simple versions
@app.on_message(filters.new_chat_members)
async def welcome(_, message):
    for m in message.new_chat_members:
        # create welcome image? simple text for now + log
        await message.reply_text(f"🎉 Welcome [{m.first_name}](tg://user?id={m.id}) to {message.chat.title}!\nEnjoy the vibe with InfinityEra 🎶")
        log_event("join", chat_id=message.chat.id, user_id=m.id)
        try:
            await app.send_message(LOG_CHANNEL, f"User joined: {m.first_name} ({m.id}) in {message.chat.title} ({message.chat.id})")
        except:
            pass

@app.on_message(filters.left_chat_member)
async def left(_, message):
    m = message.left_chat_member
    await message.reply_text(f"👋 Bye [{m.first_name}](tg://user?id={m.id}), hope to see you again in {message.chat.title} ❤️")
    log_event("leave", chat_id=message.chat.id, user_id=m.id)

# Owner-only commands: /logs /stats /broadcast /reload
@app.on_message(filters.command("stats") & filters.user(OWNER_ID))
async def stats(_, message):
    total_users = users_col.count_documents({})
    total_groups = groups_col.count_documents({})
    total_songs = songs_col.count_documents({})
    await message.reply_text(f"📊 Users: {total_users}\n💬 Groups: {total_groups}\n🎵 Songs logged: {total_songs}")

@app.on_message(filters.command("broadcast") & filters.user(OWNER_ID))
async def broadcast(_, message):
    text = " ".join(message.command[1:])
    if not text:
        await message.reply_text("Usage: /broadcast <message>")
        return
    # naive broadcast to groups saved in groups_col
    groups = groups_col.find({})
    ok = 0
    for g in groups:
        try:
            await app.send_message(int(g["chat_id"]), text)
            ok += 1
        except:
            pass
    await message.reply_text(f"Sent to {ok} chats.")

# Bot startup
async def main():
    global pytg
    await app.start()
    pytg = init_pytgcalls(app)
    await pytg.start()
    print("InfinityEra started")
    # ensure developer log channel exists? optional
    await asyncio.Future()  # run forever

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
