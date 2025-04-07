import os
import yt_dlp
from telegram import Update
from telegram.ext import ContextTypes

from list_audio import handle_audio_list
from single_audio import handle_single_audio

DOWNLOAD_DIR = "downloads"
FFMPEG_PATH = "/usr/local/bin/ffmpeg"
FFPROBE_PATH = "/usr/local/bin/ffprobe"

os.makedirs(DOWNLOAD_DIR, exist_ok=True)


async def handle_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    if "youtube.com" not in url and "youtu.be" not in url:
        await update.message.reply_text("❗ Please send a valid YouTube URL.")
        return

    status_message = await update.message.reply_text("🎧 Downloading...")

    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f'{DOWNLOAD_DIR}/%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'ffmpeg_location': FFMPEG_PATH,
            'ffprobe_location': FFPROBE_PATH,

        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            entries = info.get("entries")

            if entries:  # It's a playlist
                if len(entries) >= 20:
                    print("entries count =", len(entries))
                    raise Exception("🚫 Playlist too long!")

                await handle_audio_list(update, entries)
            else:  # It's a single video
                await handle_single_audio(info, update)

        await status_message.delete()

    except Exception as e:
        await status_message.delete()
        await update.message.reply_text(f"❌ Error: {str(e)}")
