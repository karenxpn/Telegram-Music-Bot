import os
from telegram import InputFile

async def send_audio_response(update, filename, title, performer):
    if os.path.exists(filename):
        with open(filename, 'rb') as audio_file:
            await update.message.reply_audio(
                audio=InputFile(audio_file),
                title=title,
                performer=performer
            )
        os.remove(filename)
    else:
        print(f"[ERROR] File not found: {filename}")