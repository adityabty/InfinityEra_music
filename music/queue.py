# music/queue.py

from collections import deque

# Dictionary to hold queues for different chats: {chat_id: deque([...songs])}
queues = {}

def get_queue(chat_id: int):
    """Returns the queue for a given chat_id, creating one if it doesn't exist."""
    if chat_id not in queues:
        queues[chat_id] = deque()
    return queues[chat_id]

def add_to_queue(chat_id: int, song_data: dict):
    """Adds a song to the end of the chat's queue."""
    queue = get_queue(chat_id)
    queue.append(song_data)

def get_next_song(chat_id: int):
    """Removes and returns the next song from the queue, or None if empty."""
    queue = get_queue(chat_id)
    if queue:
        return queue.popleft()
    return None

def is_queue_empty(chat_id: int):
    """Checks if the queue for a chat is empty."""
    return not bool(get_queue(chat_id))
