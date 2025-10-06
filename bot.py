from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# توکن مستقیم (فقط برای تست)
TOKEN = "8270187709:AAHdH9SaJqXFD_-FTKHkYd0QKlGtKOk8yFU"



from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = "توکن_خودتو_اینجا_بذار"

menu_keyboard = [
    ["ثبت نام", "ورود"],
    ["پشتیبانی", "تمرینات"],
    ["شکایت", "بک تست"]
]

menu_markup = ReplyKeyboardMarkup(menu_keyboard, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام! لطفا یکی از گزینه‌های زیر را انتخاب کن:",
        reply_markup=menu_markup
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "ثبت نام":
        await update.message.reply_text("شما وارد بخش ثبت نام شدید.")
        # اینجا کد ثبت نام رو بنویس
    elif text == "ورود":
        await update.message.reply_text("شما وارد بخش ورود شدید.")
        # اینجا کد ورود رو بنویس
    elif text == "پشتیبانی":
        await update.message.reply_text("چگونه می‌توانم کمکتان کنم؟")
        # کد پشتیبانی
    elif text == "تمرینات":
        await update.message.reply_text("تمرینات برای شما ارسال می‌شود.")
        # کد تمرینات
    elif text == "شکایت":
        await update.message.reply_text("لطفا شکایت خود را ارسال کنید.")
        # کد شکایت
    elif text == "بک تست":
        await update.message.reply_text("بک تست در حال آماده سازی است.")
        # کد بک تست
    else:
        await update.message.reply_text("لطفا یکی از گزینه‌های منو را انتخاب کنید.")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    app.run_polling()
