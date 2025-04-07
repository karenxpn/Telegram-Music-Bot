import os
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, MessageHandler, filters, CommandHandler
from bot_intro import start
from url_handler import handle_url

load_dotenv()
token = os.environ.get("TOKEN")


if __name__ == "__main__":
    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_url))

    app.run_polling()

