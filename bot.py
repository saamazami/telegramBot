from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# توکن مستقیم (فقط برای تست)
TOKEN = "8270187709:AAHdH9SaJqXFD_-FTKHkYd0QKlGtKOk8yFU"

# هندلر /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام سام 👋")

# اجرای ربات
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()
