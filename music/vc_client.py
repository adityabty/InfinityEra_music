# music/vc_client.py

from pytgcalls.handlers import OnGroupCall
from pytgcalls.types import Update
from main import vc_client # main.py से vc_client को आयात करें

# ... (अन्य imports जैसे logs)

@vc_client.on_kicked()
@vc_client.on_left()
@vc_client.on_closed()
async def on_vc_leave(_, update: Update):
    """VC से बाहर निकलने पर प्रतिक्रिया"""
    chat_id = update.chat_id
    await vc_client.send_message(
        chat_id,
        "😴 Bye everyone! Till next jam session 🎵"
    )
    # Log the action here (requires client object if logging to Telegram)
    # log_action_to_channel(client, ..., "LEAVE_VC", ...)

@vc_client.on_stream_end()
async def on_stream_end(_, update: Update):
    """जब गाना समाप्त हो जाता है, तो अगला गाना प्ले करें (यदि कतार में है)"""
    # Implement queue logic here
    pass
  
