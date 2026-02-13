from InflexMusic import app
from pyrogram import Client, filters
from pyrogram.types import Message
from datetime import datetime

chat_start_times = {}  # Hər qrup üçün start vaxtını yadda saxlayırıq

# Görüntülü söhbət başladıqda
@app.on_message(filters.video_chat_started & filters.group)
async def video_chat_started_handler(client: Client, message: Message):
    chat_id = message.chat.id
    text = "<b>Qrupda səsli söhbət başladı 😉</b>"
    await message.reply(text)  # Sadəcə reply edir, pin etmir
    chat_start_times[chat_id] = datetime.now()

# Görüntülü söhbət bitdikdə
@app.on_message(filters.video_chat_ended & filters.group)
async def video_chat_ended_handler(client: Client, message: Message):
    chat_id = message.chat.id

    if chat_id in chat_start_times:
        start_time = chat_start_times[chat_id]
        duration = datetime.now() - start_time
        seconds = int(duration.total_seconds())
        mins, secs = divmod(seconds, 60)
        hours, mins = divmod(mins, 60)
        duration_text = f"{hours} saat, {mins} dəqiqə, {secs} saniyə"
        del chat_start_times[chat_id]
    else:
        duration_text = "Naməlum"

    end_text = f"<b>Səsli söhbət sona çatdı 😏</b>"

    await message.reply(end_text)
