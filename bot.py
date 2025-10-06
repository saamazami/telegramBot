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

ENTERING = 1  # مرحله گرفتن اطلاعات ورود

# وقتی /start زده میشه یا هر وقت منو بخواد نمایش داده بشه
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام! منو را انتخاب کنید:",
        reply_markup=main_menu
    )

# وقتی کاربر روی "ورود" میزنه
async def login_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("لطفا شناسه یا نام کاربری خود را وارد کنید:")
    return ENTERING

# گرفتن شناسه از کاربر
async def receive_login(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    
    # اینجا درخواست به n8n (مثلا یک وب‌هوک) می‌فرستیم و نتیجه میگیریم
    n8n_webhook_url = "https://your-n8n-instance/webhook/login-check"  # این آدرس رو به آدرس درست تغییر بده
    
    try:
        response = requests.post(n8n_webhook_url, json={"username": user_input})
        data = response.json()
        
        if data.get("valid"):  # فرض میکنیم n8n جواب میده {"valid": True, "name": "اسم کاربر"}
            name = data.get("name", "کاربر")
            await update.message.reply_text(f"خوش آمدی، {name}!")
        else:
            await update.message.reply_text("شناسه معتبر نیست. لطفا دوباره تلاش کنید.")
    except Exception as e:
        await update.message.reply_text("خطا در ارتباط با سرور. لطفا بعدا تلاش کنید.")
        print(f"Error contacting n8n: {e}")
    
    # بعد از ورود یا تلاش ناموفق، منو رو دوباره بفرست
    await update.message.reply_text("منو را انتخاب کنید:", reply_markup=main_menu)
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("عملیات لغو شد.", reply_markup=main_menu)
    return ConversationHandler.END

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex('^(ورود)$'), login_start)],
        states={
            ENTERING: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_login)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv_handler)

    app.run_polling()

if __name__ == "__main__":
    main()

