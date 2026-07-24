import os
import asyncio
import threading
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("BOT_TOKEN")

app_web = Flask(__name__)

@app_web.route("/")
def home():
    return "Bot ishlayapti ✅"

def run_web():
    app_web.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Bot ishlayapti ✅\n"
        "SofaScore rasmini yuboring 📷"
    )


async def photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Rasm qabul qilindi ✅\n"
        "Keyingi bosqichda tahlil qo‘shiladi."
    )


async def main():
    bot = Application.builder().token(TOKEN).build()

    bot.add_handler(CommandHandler("start", start))
    bot.add_handler(MessageHandler(filters.PHOTO, photo))

    await bot.initialize()
    await bot.start()
    await bot.updater.start_polling()

    await asyncio.Event().wait()


if __name__ == "__main__":
    threading.Thread(target=run_web).start()
    asyncio.run(main())
