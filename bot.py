from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

import os

TOKEN = os.getenv("TOKEN") or "توکن‌تو اینجا بذار فقط برای تست"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام سام 👋")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()
