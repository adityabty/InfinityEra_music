@Client.on_message(filters.left_chat_members & filters.group)
async def say_goodbye(client, message):
    for member in message.left_chat_members:
        if member.id == client.me.id:
            # Bot was removed logic (e.g., log to channel)
            continue
            
        mention = member.mention
        chat_title = message.chat.title
        
        # 1. Log event
        # ... log_action_to_mongodb()
        
        # 2. Send Message
        await message.reply_text(
            f"👋 Bye {mention}, hope to see you again in {chat_title} ❤️"
        )
      
