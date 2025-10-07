import os
import re
import requests
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    ConversationHandler,
    filters,
)

# مراحل
(
    CHOOSING,
    SIGNUP_NAME,
    SIGNUP_TELEGRAM,
    SIGNUP_PHONE,
    SIGNUP_EMAIL,
    SIGNUP_INSTAGRAM,
    CONFIRMATION
) = range(7)

# وب‌هوک n8n خودت رو بذار اینجا
N8N_WEBHOOK_URL = "https://n8n.example.com/webhook/register-user"

main_menu_keyboard = [
    ["ثبت نام", "ورود"],
    ["پشتیبانی", "تمرینات"],
    ["شکایت", "بک تست"]
]
main_menu_markup = ReplyKeyboardMarkup(main_menu_keyboard, resize_keyboard=True)

# تایید یا رد اطلاعات
confirm_keyboard = [
    ["✅ تایید و ثبت", "🔁 ویرایش اطلاعات"]
]
confirm_markup = ReplyKeyboardMarkup(confirm_keyboard, resize_keyboard=True)

# اعتبارسنجی‌ها
def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email)

def is_valid_phone(phone):
    return phone.isdigit() and len(phone) == 11

def send_to_n8n(data):
    try:
        response = requests.post(N8N_WEBHOOK_URL, json=data)
        print("✅ Sent to n8n:", response.status_code)
        return response.status_code == 200
    except Exception as e:
        print("❌ Error sending to n8n:", e)
        return False

# شروع
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام! لطفا یکی از گزینه‌های زیر را انتخاب کنید:",
        reply_markup=main_menu_markup
    )
    return CHOOSING

# شروع ثبت نام
async def handle_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "ثبت نام":
        await update.message.reply_text("لطفاً نام کامل خود را وارد کنید:")
        return SIGNUP_NAME
    else:
        await update.message.reply_text("این گزینه هنوز فعال نیست.")
        return CHOOSING

# گرفتن اطلاعات
async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text
    await update.message.reply_text("آیدی تلگرام خود را وارد کنید (با @):")
    return SIGNUP_TELEGRAM

async def get_telegram_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["telegram_id"] = update.message.text
    await update.message.reply_text("شماره تلفن خود را وارد کنید:")
    return SIGNUP_PHONE

async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    phone = update.message.text
    if not is_valid_phone(phone):
        await update.message.reply_text("❌ شماره تلفن باید عدد و ۱۱ رقمی باشد. لطفاً دوباره وارد کنید:")
        return SIGNUP_PHONE

    context.user_data["phone"] = phone
    await update.message.reply_text("ایمیل خود را وارد کنید:")
    return SIGNUP_EMAIL

async def get_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    email = update.message.text
    if not is_valid_email(email):
        await update.message.reply_text("❌ فرمت ایمیل معتبر نیست. لطفاً دوباره وارد کنید:")
        return SIGNUP_EMAIL

    context.user_data["email"] = email
    await update.message.reply_text("آیدی اینستاگرام خود را وارد کنید (بدون @):")
    return SIGNUP_INSTAGRAM

async def get_instagram(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["instagram"] = update.message.text

    data = context.user_data
    msg = (
        "✅ لطفاً اطلاعات زیر را بررسی کنید:\n"
        f"👤 نام: {data['name']}\n"
        f"📱 تلگرام: {data['telegram_id']}\n"
        f"📞 شماره: {data['phone']}\n"
        f"📧 ایمیل: {data['email']}\n"
        f"📸 اینستا: {data['instagram']}\n\n"
        "آیا این اطلاعات صحیح هستند؟"
    )

    await update.message.reply_text(msg, reply_markup=confirm_markup)
    return CONFIRMATION

# تایید یا رد
async def handle_confirmation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    choice = update.message.text
    if choice == "✅ تایید و ثبت":
        user = update.effective_user
        data = {
            "id": user.id,
            "name": context.user_data.get("name"),
            "email": context.user_data.get("email"),
            "phone": context.user_data.get("phone"),
            "telegram_id": context.user_data.get("telegram_id"),
            "instagram": context.user_data.get("instagram")
        }
        send_to_n8n(data)

        await update.message.reply_text("✅ اطلاعات با موفقیت ثبت شد.")
        await update.message.reply_text("⏳ لطفاً منتظر باشید تا آیدی شما ساخته شده و در تلگرام برای شما ارسال شود.", reply_markup=main_menu_markup)
        return CHOOSING

    elif choice == "🔁 ویرایش اطلاعات":
        await update.message.reply_text("باشه! بیایید از اول شروع کنیم.\nلطفاً نام کامل خود را وارد کنید:", reply_markup=ReplyKeyboardRemove())
        return SIGNUP_NAME

    else:
        await update.message.reply_text("لطفاً یکی از گزینه‌های بالا را انتخاب کنید:")
        return CONFIRMATION

# Conversation Handler
conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        CHOOSING: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_choice)],
        SIGNUP_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
        SIGNUP_TELEGRAM: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_telegram_id)],
        SIGNUP_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)],
        SIGNUP_EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_email)],
        SIGNUP_INSTAGRAM: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_instagram)],
        CONFIRMATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_confirmation)],
    },
    fallbacks=[CommandHandler("start", start)],
)

# اجرای ربات
if __name__ == "__main__":
    TOKEN = os.getenv("TOKEN")  # یا مستقیم مقدارش رو بذار: '123456:ABCDEF...'
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(conv_handler)
    app.run_polling()
