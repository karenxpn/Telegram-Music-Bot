import os

import yt_dlp
from dotenv import load_dotenv

from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

load_dotenv()
token = os.environ.get("TOKEN")
DOWNLOAD_DIR = "downloads"
FFMPEG_PATH = "/usr/local/bin/ffmpeg"
FFPROBE_PATH = "/usr/local/bin/ffprobe"

os.makedirs(DOWNLOAD_DIR, exist_ok=True)


async def handle_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    if "youtube.com" not in url and "youtu.be" not in url:
        await update.message.reply_text("❗ Please send a valid YouTube URL.")
        return

    await update.message.reply_text("🎧 Downloading and converting...")

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
            title = info.get('title', 'audio')
            performer = info.get('uploader', 'Unknown Artist')
            filename = f"{DOWNLOAD_DIR}/{title}.mp3"

        # Send as Telegram Audio (with metadata)
        with open(filename, 'rb') as audio_file:
            await update.message.reply_audio(
                audio=InputFile(audio_file),
                title=title,
                performer=performer
            )

        os.remove(filename)

    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(token).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_url))
    app.run_polling()

