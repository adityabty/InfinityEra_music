from pyrogram import Client, filters
# मान लें कि आपके पास ये सहायक फ़ंक्शन हैं:
# from utils.image_generator import generate_welcome_image 
# from database.logs import log_action_to_channel

@Client.on_message(filters.new_chat_members & filters.group)
async def welcome_new_member(client, message):
    for member in message.new_chat_members:
        if member.is_bot:
            # Bot joined group logic (e.g., log, send initial instructions)
            continue

        # Get chat info and member count
        chat = await client.get_chat(message.chat.id)
        
        # 1. Generate Welcome Image (Mock Logic)
        # image_path = await generate_welcome_image(member, chat.members_count)

        # 2. Log event
        await log_action_to_channel(
            client, 
            message.chat.id, 
            member.id, 
            "USER_JOIN", 
            member.first_name
        )

        # 3. Send Message
        mention = member.mention
        caption = f"🎉 Welcome {mention} to **{chat.title}**! Enjoy the vibe with InfinityEra 🎶"
        
        # await client.send_photo(
        #     message.chat.id,
        #     photo=image_path,
        #     caption=caption
        # )
        
        # Temporary text reply
        await message.reply_text(caption)
      
