from pyrogram import Client, filters

@Client.on_message(filters.document | filters.video | filters.audio)
async def auto_add_file(client, message: Message):
    file_name = message.document.file_name if message.document else (
        message.video.file_name if message.video else message.audio.file_name
    )

    if not file_name:
        return

    query = file_name.rsplit(".", 1)[0]  # File ka naam extension ke bina
    file_id = message.document.file_id if message.document else (
        message.video.file_id if message.video else message.audio.file_id
    )

    # (Yahan file ko tumhare database me add karne ka existing process hoga)

    # Check karo ki koi user pehle is file ko search kar chuka tha
    missing_data = await missing_requests_col.find_one({"query": query})
    if missing_data:
        users_to_notify = missing_data["users"]

        for user_id in users_to_notify:
            try:
                await client.send_message(
                    user_id,
                    f"✅ **Your requested file is now available!**\n"
                    f"🔍 Search again in our group:",
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("🔍 Search Now", url="t.me/yourgroup")]
                    ])
                )
            except Exception as e:
                print(f"Failed to notify {user_id}: {e}")

        # Notification bhejne ke baad query ko remove kar dete hain
        await missing_requests_col.delete_one({"query": query})

    await message.reply_text("✅ File successfully added to database!")
