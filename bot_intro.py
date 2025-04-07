from telegram import Update
from telegram.ext import ContextTypes


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "🎵 **Welcome to YouTube MP3 Bot!**\n"
        "Just send me any YouTube video or playlist link, and I’ll convert it to high-quality MP3 and send it back to you — fast and easy.\n\n"
        "✅ **What I support:**\n"
        "- Single YouTube videos 🎥\n"
        "- Audio files in **MP3 format** 🎧\n\n"
        "🚀 **How to use:**\n"
        "1. Copy the YouTube video or playlist URL\n"
        "2. Paste it here\n"
        "3. Wait a moment while I process and send your audio"
    )
    await update.message.reply_markdown(welcome_text)
