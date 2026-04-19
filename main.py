import logging
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

# --- الإعدادات (ضع توكن بوتك هنا) ---
BOT_TOKEN = "8650385840:AAGVHWVbQ0MzirtA_l6-S83HNKL1O7Jrk2g" 
CHANNELS_TO_CHECK = ["@ddev8"]
YOUTUBE_URL = "https://youtube.com/@devinstagram?si=e9YNvnDylP2wC4XL"
TELEGRAM_URL = "https://t.me/ddev8"
SUPPORT_URL = "https://t.me/iidevv"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# --- دالة التحقق من الاشتراك ---
async def is_subscribed(user_id: int):
    for channel in CHANNELS_TO_CHECK:
        try:
            member = await bot.get_chat_member(chat_id=channel, user_id=user_id)
            if member.status in ["member", "administrator", "creator"]:
                return True
        except Exception:
            return False
    return False

# --- لوحات المفاتيح (Keyboards) ---
def get_subscription_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Subscribe to Telegram", url=TELEGRAM_URL))
    builder.row(InlineKeyboardButton(text="Subscribe to YouTube", url=YOUTUBE_URL))
    builder.row(InlineKeyboardButton(text="Verify Subscription ✅", callback_data="verify_sub"))
    return builder.as_markup()

def get_language_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="English 🇺🇸", callback_data="lang_en"),
        InlineKeyboardButton(text="عربي 🇸🇦", callback_data="lang_ar")
    )
    return builder.as_markup()

def get_main_keyboard(lang):
    builder = InlineKeyboardBuilder()
    if lang == "ar":
        builder.row(InlineKeyboardButton(text="الإيميلات", callback_data="emails"))
        builder.row(InlineKeyboardButton(text="الرسالة", callback_data="msg_ar"))
        builder.row(InlineKeyboardButton(text="💰 الفك المدفوع", callback_data="paid_service"))
    else:
        builder.row(InlineKeyboardButton(text="Emails", callback_data="emails"))
        builder.row(InlineKeyboardButton(text="Message", callback_data="msg_en"))
        builder.row(InlineKeyboardButton(text="💰 Paid Service", callback_data="paid_service"))
    return builder.as_markup()

def get_support_keyboard(lang):
    builder = InlineKeyboardBuilder()
    btn_text = "تواصل معي الآن" if lang == "ar" else "Contact Me Now"
    builder.row(InlineKeyboardButton(text=btn_text, url=SUPPORT_URL))
    return builder.as_markup()

# --- Handlers ---

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    if await is_subscribed(message.from_user.id):
        await message.answer("Please choose your language / الرجاء اختيار اللغة:", reply_markup=get_language_keyboard())
    else:
        await message.answer("يجب الاشتراك في قنواتنا أولاً لاستخدام البوت.\nYou must subscribe to our channels first.", reply_markup=get_subscription_keyboard())

@dp.callback_query(F.data == "verify_sub")
async def verify_sub_handler(callback: types.CallbackQuery):
    if await is_subscribed(callback.from_user.id):
        await callback.message.edit_text("Success! Choose language / تم التحقق! اختر اللغة:", reply_markup=get_language_keyboard())
    else:
        await callback.answer("لم تشترك بعد! / Not subscribed yet!", show_alert=True)

@dp.callback_query(F.data.startswith("lang_"))
async def set_language(callback: types.CallbackQuery):
    lang = callback.data.split("_")[1]
    text = "أهلاً بك! اختر أحد الخيارات:" if lang == "ar" else "Welcome! Choose an option:"
    await callback.message.edit_text(text, reply_markup=get_main_keyboard(lang))

@dp.callback_query(F.data == "paid_service")
async def paid_service_handler(callback: types.CallbackQuery):
    ad_text = (
        "🔥 **فك باند حسابات أنستقرام مدفوع**\n\n"
        "✅ جميع انواع الباند\n"
        "🚀 ضمان فك الباند بأسرع وقت\n"
        "💸 أسعار رخيصه ومناسبة"
    )
    # نحدد لغة زر التواصل بناءً على آخر رسالة
    lang = "ar" if "أهلاً" in callback.message.text else "en"
    await callback.message.answer(ad_text, reply_markup=get_support_keyboard(lang), parse_mode="Markdown")
    await callback.answer()

@dp.callback_query(F.data == "emails")
async def show_emails(callback: types.CallbackQuery):
    emails_text = "security@mail.instagram.com\nappeals@instagram.com\nsupport@instagram.com"
    await callback.message.answer(emails_text)
    await callback.answer()

@dp.callback_query(F.data == "msg_en")
async def show_msg_en(callback: types.CallbackQuery):
    full_msg_en = (
        "Subject: Request for Manual Review and Reinstatement of My Disabled Instagram Account\n\n"
        "Dear Instagram / Meta Support Team,\n"
        "I hope this message finds you well.\n"
        "My name is [Full Name exactly as in Passport/ID]. I am writing to respectfully appeal the decision to disable my Instagram account.\n"
        "I recently discovered that my account has been disabled when I attempted to log in. I was very surprised by this action because I have always used Instagram responsibly and in full compliance with the Community Guidelines and Terms of Service. To the best of my knowledge, I have not posted any content that violates your policies, nor have I engaged in any prohibited activities such as spam, harassment, or other violations.\n"
        "This account is very important to me. It contains many years of personal memories, photos, videos, and connections with friends and family. Losing access to it has caused me significant inconvenience, and I kindly request that your team perform a thorough manual review of the account to reconsider the disablement decision.\n"
        "I understand that automated systems can sometimes flag accounts in error, and I sincerely believe this may be the case here. I am fully committed to continuing to follow all of Instagram’s rules and guidelines if my account is reinstated. I am also ready and willing to provide any additional verification or information that may be required, including:\n"
        "• A clear video selfie for identity confirmation\n"
        "• A copy of my government-issued identification (such as passport or national ID card)\n"
        "• Any other details needed to confirm that I am the legitimate owner of the account\n"
        "I have been accessing and using this account consistently from my usual devices and location in Amman, Jordan, without any previous issues. Thank you sincerely for taking the time to review my case. I truly value the Instagram community and would be extremely grateful if you could restore access to my account at your earliest convenience.\n\n"
        "Best regards,\n"
        "[Full Name]\n"
        "Email address associated with the account: [Email]\n"
        "Phone number (if associated): [Phone Number]"
    )
    await callback.message.answer(full_msg_en)
    await callback.answer()

@dp.callback_query(F.data == "msg_ar")
async def show_msg_ar(callback: types.CallbackQuery):
    full_msg_ar = (
        "الموضوع: طلب مراجعة يدوية واستعادة حسابي المعطل على إنستغرام\n\n"
        "فريق دعم إنستغرام / ميتا المحترمين،\n"
        "اسمي الكامل: [اكتب اسمك كما في الهوية]. أراسلكم لاستئناف قرار تعطيل حسابي.\n"
        "لقد اكتشفت مؤخراً تعطيل حسابي، وأنا متأكد أنني ملتزم بجميع القوانين ولم أنتهك معايير المجتمع. هذا الحساب يحتوي على ذكريات شخصية وصور تهمنا جداً.\n"
        "أنا على استعداد لتقديم كافة الإثباتات المطلوبة لتأكيد هويتي، بما في ذلك فيديو سيلفي وصورة الهوية الشخصية (جواز سفر أو بطاقة شخصية).\n"
        "أستخدم هذا الحساب من أجهزتي المعتادة في عمان، الأردن، ولم أواجه أي مشاكل سابقاً. أرجو مراجعة طلبي وإعادة الحساب في أقرب وقت.\n\n"
        "مع خالص التقدير،\n"
        "[اسمك الكامل]\n"
        "الإيميل المرتبط بالحساب: [إيميل الحساب]\n"
        "رقم الهاتف: [رقم الهاتف]"
    )
    await callback.message.answer(full_msg_ar)
    await callback.answer()

# --- Main ---
async def main():
    logging.basicConfig(level=logging.INFO)
    print("--- Bot is Running with Paid Service Feature ---")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass
