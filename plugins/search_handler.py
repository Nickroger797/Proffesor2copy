from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

MISSING_FILES_CHANNEL = -1001234567890  # Yahan apne channel ka ID dalna

@Client.on_message(filters.text & filters.group)
async def search_file(client, message: Message):
    query = message.text.strip()
    user = message.from_user

    # Database me search karo
    results = await search_database(query)

    if not results:
        log_text = (
            f"📢 **File Not Found in Database**\n"
            f"👤 **User:** {user.first_name} (`{user.id}`)\n"
            f"🔍 **Search Query:** `{query}`\n"
            f"🕒 **Time:** {message.date}"
        )
        await client.send_message(MISSING_FILES_CHANNEL, log_text)  

        # Agar pehle se missing request hai to update karo, nahi to naya add karo
        existing = await missing_requests_col.find_one({"query": query})
        if not existing:
            await missing_requests_col.insert_one({"query": query, "users": [user.id]})
        else:
            await missing_requests_col.update_one(
                {"query": query},
                {"$addToSet": {"users": user.id}}
            )

        await message.reply_text("❌ Sorry, yeh file database me nahi mili!")
        return

    await send_results(client, message, results)
