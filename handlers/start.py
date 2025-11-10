from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.logs import log_action_to_channel # मान लें कि यह फ़ंक्शन logs.py में है
from config import DEVELOPER_USER, SUPPORT_CHAT, UPDATE_CHANNEL

@Client.on_message(filters.command("start"))
async def start_command(client, message):
    # Log /start usage
    await log_action_to_channel(
        client, 
        message.chat.id, 
        message.from_user.id, 
        "START_COMMAND", 
        "N/A"
    )

    # Inline Keyboard
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("👨‍💻 Developer", url=f"https://t.me/{DEVELOPER_USER}"),
                InlineKeyboardButton("📢 Updates", url=UPDATE_CHANNEL),
            ],
            [
                InlineKeyboardButton("💬 Support", url=SUPPORT_CHAT),
                InlineKeyboardButton("➕ Add Me To Group", url=f"https://t.me/{client.me.username}?startgroup=true"),
            ]
        ]
    )

    # Message
    await message.reply_text(
        "🎵 Welcome to **InfinityEra Bot**\nSweet, Smart & Stylish Music for Your Telegram VC.",
        reply_markup=keyboard
    )
  
