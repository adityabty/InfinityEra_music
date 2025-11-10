# music_player.py
import os
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import AudioPiped
from pyrogram import Client
from config import DOWNLOADS_DIR
from db import log_event, songs_col
from collections import defaultdict

# We'll create an instance of PyTgCalls later from main.py
# Maintain per-chat current track info
now_playing = {}   # chat_id -> {path, title, requester_id}

def init_pytgcalls(app: Client):
    call = PyTgCalls(app)
    return call

async def play_track(call: PyTgCalls, chat_id: int, file_path: str, title: str, requester):
    """
    Join VC and play the provided local audio file via AudioPiped.
    """
    audio = AudioPiped(file_path)
    # join & start
    await call.join_group_call(chat_id, audio)
    now_playing[chat_id] = {"path": file_path, "title": title, "requester": requester}
    # log
    log_event("play", chat_id=chat_id, user_id=requester.id if requester else None, song_name=title)

async def pause(chat_id, call):
    try:
        await call.pause_stream(chat_id)
    except Exception as e:
        raise

async def resume(chat_id, call):
    try:
        await call.resume_stream(chat_id)
    except Exception as e:
        raise

async def stop(chat_id, call):
    try:
        await call.leave_group_call(chat_id)
        if chat_id in now_playing:
            del now_playing[chat_id]
    except Exception as e:
        raise
