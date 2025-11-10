# handlers/help.py

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import DEVELOPER_USER, SUPPORT_CHAT, UPDATE_CHANNEL

@Client.on_message(filters.command("help"))
async def help_command(client, message):
    
    help_text = """
🎛️ **InfinityEra Group Help Bot – Main Functions**

1️⃣ **Moderation**
 • Remove spam and links
 • Filter abusive words
 • Control message flooding

2️⃣ **User Management**
 • Kick/Ban/Warn users
 • Auto warn-limit actions
 • Send welcome messages

3️⃣ **Security & Utilities**
 • Captcha verification
 • /rules, /about
 • Protect group settings

4️⃣ **Music Player (VC)**
 • /play: Play requested song from YouTube
 • /skip, /pause, /resume, /stop: Control playback
 • Queue management (Upcoming)
"""

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("💬 Support", url=SUPPORT_CHAT),
                InlineKeyboardButton("📢 Updates", url=UPDATE_CHANNEL),
            ],
            [
                InlineKeyboardButton("🧑‍💻 Developer", url=f"https://t.me/{DEVELOPER_USER}"),
                InlineKeyboardButton("❌ Close", callback_data="close_help_message"),
            ]
        ]
    )

    await message.reply_text(
        help_text,
        reply_markup=keyboard,
        disable_web_page_preview=True
    )

# Optional: Add a handler to close the help message
@Client.on_callback_query(filters.regex("close_help_message"))
async def close_help_callback(_, callback_query):
    await callback_query.message.delete()
    await callback_query.answer("Help message closed.")
  
