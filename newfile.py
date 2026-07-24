import os
import asyncio
import threading
from flask import Flask
from PIL import Image
import pytesseract
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
    photo = await update.message.photo[-1].get_file()

    file_path = "sofascore.png"
    await photo.download_to_drive(file_path)

    text = pytesseract.image_to_string(
        Image.open(file_path),
        lang="eng"
    )

    if text.strip():
        await update.message.reply_text(
            "O‘qilgan matn:\n\n" + text[:4000]
        )
    else:
        await update.message.reply_text(
            "Rasmdan matn topilmadi ❌"
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
