# music/controls.py

from pyrogram import Client, filters
from pyrogram.types import CallbackQuery
from main import vc_client # PyTgCalls client
import os 

@Client.on_callback_query(filters.regex("^controls_"))
async def music_controls_callback(client: Client, callback_query: CallbackQuery):
    data = callback_query.data.split("_")[1]
    chat_id = callback_query.message.chat.id
    user_id = callback_query.from_user.id
    
    # Optional: Only allow the user who requested the song, or admins, to control.
    # For simplicity, we skip admin check for now.
    
    try:
        if data == "pause":
            await vc_client.pause_stream(chat_id)
            await callback_query.answer("⏸ Playback Paused!", show_alert=False)
            
        elif data == "resume":
            await vc_client.resume_stream(chat_id)
            await callback_query.answer("▶️ Playback Resumed!", show_alert=False)
            
        elif data == "skip":
            # Real skip implementation requires queue logic. 
            # For now, we just stop the current stream.
            await vc_client.leave_group_call(chat_id) # Stops and leaves
            await client.send_message(chat_id, "⏩ Song Skipped/Stopped. Next song in queue will play (Queue logic required).")
            await callback_query.answer("⏩ Skipping Song...", show_alert=False)
            
        elif data == "stop":
            await vc_client.leave_group_call(chat_id)
            await client.send_message(
                chat_id, 
                "⏹ Playback stopped and bot left VC. 😴 Bye everyone! Till next jam session 🎵"
            )
            await callback_query.answer("⏹ Playback Stopped.", show_alert=False)
            
        elif data == "close":
            await callback_query.message.delete()
            await callback_query.answer("❌ Message Closed.", show_alert=False)

    except Exception as e:
        # Handle cases where VC is already stopped or bot is not in VC
        await callback_query.answer("⚠️ Error: Bot might not be in VC or stream is already managed.", show_alert=True)
        print(f"Control callback error: {e}")
          
