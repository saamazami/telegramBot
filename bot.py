import os
import re
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
    ConversationHandler
)
import logging

# لاگ برای دیباگ راحت‌تر
logging.basicConfig(level=logging.INFO)

# --- توابع اعتبارسنجی ---

def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email)

def is_valid_phone(phone):
    return phone.isdigit() and len(phone) == 11

# --- مراحل کانورسیشن ---
(
    CHOOSING,
    LOGIN,
    SIGNUP_NAME,
    SIGNUP_TELEGRAM,
    SIGNUP_PHONE,
    SIGNUP_EMAIL,
    SIGNUP_INSTAGRAM
) = range(7)

# --- توکن ربات از متغیر محیطی ---
TOKEN = os.getenv("TOKEN")  # یا مستقیم '123456:ABCDEF...' برای تست

# --- منوی اصلی ---
main_menu_keyboard = [
    ["ثبت نام", "ورود"],
    ["پشتیبانی", "تمرینات"],
    ["شکایت", "بک تست"]
]
main_menu_markup = ReplyKeyboardMarkup(main_menu_keyboard, resize_keyboard=True)

# --- Start ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام! لطفا یکی از گزینه‌های زیر را انتخاب کنید:",
        reply_markup=main_menu_markup
    )
    return CHOOSING

# --- انتخاب از منو ---
async def handle_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_choice = update.message.text

    if user_choice == "ورود":
        await update.message.reply_text("فعلاً ورود پیاده‌سازی نشده.")
        return CHOOSING

    elif user_choice == "ثبت نام":
        await update.message.reply_text("لطفاً نام کامل خود را وارد کنید:")
        return SIGNUP_NAME

    elif user_choice == "پشتیبانی":
        await update.message.reply_text("برای پشتیبانی با @support تماس بگیرید.")
        return CHOOSING

    elif user_choice == "تمرینات":
        await update.message.reply_text("تمرینات به‌زودی اضافه خواهد شد.")
        return CHOOSING

    elif user_choice == "شکایت":
        await update.message.reply_text("لطفاً شکایت خود را به آیدی @complaints ارسال کنید.")
        return CHOOSING

    elif user_choice == "بک تست":
        await update.message.reply_text("بک‌تست در حال توسعه است.")
        return CHOOSING

    else:
        await update.message.reply_text("لطفاً یک گزینه معتبر از منو انتخاب کنید.")
        return CHOOSING

# --- ثبت‌نام: مرحله 1: نام ---
async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text
    await update.message.reply_text("آیدی تلگرام خود را وارد کنید (با @):")
    return SIGNUP_TELEGRAM

# --- ثبت‌نام: مرحله 2: آیدی تلگرام ---
async def get_telegram_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["telegram_id"] = update.message.text
    await update.message.reply_text("شماره تلفن خود را وارد کنید:")
    return SIGNUP_PHONE

# --- ثبت‌نام: مرحله 3: شماره تلفن ---
async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    phone = update.message.text
    if not is_valid_phone(phone):
        await update.message.reply_text("❌ شماره تلفن باید عدد و ۱۱ رقمی باشد. لطفاً دوباره وارد کنید:")
        return SIGNUP_PHONE

    context.user_data["phone"] = phone
    await update.message.reply_text("ایمیل خود را وارد کنید:")
    return SIGNUP_EMAIL

# --- ثبت‌نام: مرحله 4: ایمیل ---
async def get_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    email = update.message.text
    if not is_valid_email(email):
        await update.message.reply_text("❌ فرمت ایمیل معتبر نیست. لطفاً دوباره وارد کنید:")
        return SIGNUP_EMAIL

    context.user_data["email"] = email
    await update.message.reply_text("آیدی اینستاگرام خود را وارد کنید (بدون @):")
    return SIGNUP_INSTAGRAM

# --- ثبت‌نام: مرحله 5: آیدی اینستاگرام ---
async def get_instagram(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["instagram"] = update.message.text

    data = context.user_data
    msg = (
        "✅ اطلاعات ثبت‌نام:\n"
        f"👤 نام: {data['name']}\n"
        f"📱 تلگرام: {data['telegram_id']}\n"
        f"📞 شماره: {data['phone']}\n"
        f"📧 ایمیل: {data['email']}\n"
        f"📸 اینستا: {data['instagram']}"
    )

    await update.message.reply_text(msg)
    await update.message.reply_text("✅ ثبت‌نام با موفقیت انجام شد.")
    await update.message.reply_text("⏳ لطفاً منتظر باشید تا آیدی شما ساخته شده و در تلگرام برای شما ارسال شود.", reply_markup=main_menu_markup)

    # اینجا می‌تونی اطلاعات رو به API یا دیتابیس بفرستی

    return CHOOSING

# --- Conversation Handler ---
conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        CHOOSING: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_choice)],
        SIGNUP_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
        SIGNUP_TELEGRAM: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_telegram_id)],
        SIGNUP_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)],
        SIGNUP_EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_email)],
        SIGNUP_INSTAGRAM: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_instagram)],
    },
    fallbacks=[],
)

# --- اجرای ربات ---
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(conv_handler)
    app.run_polling()
