ببین من یک بات ساختم و با پایتون این کد هم زدم و منو رو دارم from telegram import Update, ReplyKeyboardMarkup
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
