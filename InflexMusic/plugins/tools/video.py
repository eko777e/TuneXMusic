import os
from pyrogram import enums, filters
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputMediaVideo,
    Message,
)
from config import BANNED_USERS, SONG_DOWNLOAD_DURATION, SONG_DOWNLOAD_DURATION_LIMIT
from InflexMusic import YouTube, app
from InflexMusic.utils.decorators.language import language, languageCB

# 🔎 YouTube search (yt-dlp)
import yt_dlp

async def search_youtube(query: str, limit: int = 10):
    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "extract_flat": True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch{limit}:{query}", download=False)
        results = []
        for entry in info.get("entries", []):
            results.append({
                "title": entry.get("title"),
                "id": entry.get("id"),
                "duration": entry.get("duration"),
                "thumbnail": entry.get("thumbnail"),
            })
        return results


# ================= PRIVATE VIDEO COMMAND ================= #

@app.on_message(
    filters.command(["video"]) & filters.private & ~BANNED_USERS
)
@language
async def video_command_private(client, message: Message, _):
    if len(message.command) < 2:
        return await message.reply_text("Video adı yazın.")

    query = message.text.split(None, 1)[1]
    mystic = await message.reply_text("🔎 Axtarılır...")

    try:
        title, duration_min, duration_sec, thumbnail, vidid = await YouTube.details(query)
    except:
        return await mystic.edit_text("❌ Tapılmadı.")

    if int(duration_sec) > SONG_DOWNLOAD_DURATION_LIMIT:
        return await mystic.edit_text(
            f"❌ Video limiti keçdi.\nLimit: {SONG_DOWNLOAD_DURATION} dəq"
        )

    buttons = [
        [
            InlineKeyboardButton(
                text="🎬 Video Yüklə",
                callback_data=f"video_download {vidid}",
            ),
        ]
    ]

    await mystic.delete()
    return await message.reply_photo(
        thumbnail,
        caption=f"🎬 {title}",
        reply_markup=InlineKeyboardMarkup(buttons),
    )


# ================= VIDEO DOWNLOAD CALLBACK ================= #

@app.on_callback_query(filters.regex(pattern=r"video_download") & ~BANNED_USERS)
@languageCB
async def video_download_cb(client, CallbackQuery, _):
    try:
        await CallbackQuery.answer("🎬 Yüklənir...")
    except:
        pass

    vidid = CallbackQuery.data.split(None, 1)[1]
    yturl = f"https://www.youtube.com/watch?v={vidid}"

    mystic = await CallbackQuery.edit_message_text("📥 Video yüklənir...")

    try:
        file_path, status = await YouTube.download(
            yturl,
            mystic,
            songvideo=True,
            songaudio=None,
            title=None,
        )
    except Exception as e:
        return await mystic.edit_text(f"❌ Xəta:\n{e}")

    if not status or not file_path:
        return await mystic.edit_text("❌ Yükləmə alınmadı.")

    title, duration_min, duration_sec, thumbnail, vidid = await YouTube.details(yturl)
    thumb_image_path = await CallbackQuery.message.download()

    med = InputMediaVideo(
        media=file_path,
        duration=duration_sec,
        thumb=thumb_image_path,
        caption=f"🎬 {title}",
        supports_streaming=True,
    )

    await mystic.edit_text("📤 Video göndərilir...")

    await app.send_chat_action(
        chat_id=CallbackQuery.message.chat.id,
        action=enums.ChatAction.UPLOAD_VIDEO,
    )

    try:
        await CallbackQuery.edit_message_media(media=med)
    except Exception:
        return await mystic.edit_text("❌ Göndərilə bilmədi.")

    os.remove(file_path)
