from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
    ConversationHandler
)
import requests

# مراحل کانورسیشن
CHOOSING, LOGIN = range(2)

# توکن رو از متغیر محیطی می‌خونیم (ایمن‌تره)
TOKEN = os.getenv("TOKEN")

# منوی اصلی به صورت کیبورد
main_menu_keyboard = [
    ["ثبت نام", "ورود"],
    ["پشتیبانی", "تمرینات"],
    ["شکایت", "بک تست"]
]
main_menu_markup = ReplyKeyboardMarkup(main_menu_keyboard, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # وقتی کاربر وارد شد، منو رو نشون بده
    await update.message.reply_text(
        "سلام! لطفا یکی از گزینه‌های زیر را انتخاب کنید:",
        reply_markup=main_menu_markup
    )
    return CHOOSING

async def handle_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "ورود":
        await update.message.reply_text("لطفا نام کاربری خود را وارد کنید:")
        return LOGIN
    else:
        # برای سایر گزینه‌ها فقط یه پاسخ ساده می‌دیم (می‌تونی توسعه بدی)
        await update.message.reply_text(f"شما گزینه‌ی {text} را انتخاب کردید. فعلا در حال توسعه است.")
        return CHOOSING

async def login(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.message.text
    # اینجا باید به n8n درخواست بفرستی برای چک کردن نام کاربری
    # مثلا فرض کن n8n یه API داره به این آدرس:
    n8n_api_url = "https://your-n8n-instance.com/webhook/check_login"
    try:
        response = requests.post(n8n_api_url, json={"username": username})
        response_data = response.json()
        if response.status_code == 200 and response_data.get("valid"):
            await update.message.reply_text(f"خوش آمدید {username} عزیز! شما با موفقیت وارد شدید.")
        else:
            await update.message.reply_text("نام کاربری یا رمز عبور اشتباه است. لطفا دوباره تلاش کنید.")
    except Exception as e:
        await update.message.reply_text("خطایی رخ داد، لطفا بعدا دوباره تلاش کنید.")
        print(e)

    # بعد از ورود یا خطا برمی‌گردیم به منو
    await update.message.reply_text(
        "لطفا یکی از گزینه‌های زیر را انتخاب کنید:",
        reply_markup=main_menu_markup
    )
    return CHOOSING

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("عملیات لغو شد. برای شروع مجدد /start را بزنید.")
    return ConversationHandler.END

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOOSING: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_choice)],
            LOGIN: [MessageHandler(filters.TEXT & ~filters.COMMAND, login)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    app.add_handler(conv_handler)

    print("Bot is running...")
    app.run_polling()

if __name__ == '__main__':
    main()

