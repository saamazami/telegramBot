import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# توکن رو از متغیر محیطی می‌خونیم (ایمن‌تره)
TOKEN = os.getenv("TOKEN")

# تعریف منوی اصلی با دکمه‌ها
main_menu = ReplyKeyboardMarkup(
    [
        ["ثبت نام", "ورود"],
        ["پشتیبانی", "تمرینات"],
        ["شکایت", "بک تست"]
    ],
    resize_keyboard=True
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "لطفا یکی از گزینه‌های زیر را انتخاب کنید:",
        reply_markup=main_menu
    )

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()

if __name__ == "__main__":
    main()
