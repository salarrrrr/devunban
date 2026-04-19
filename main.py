import os
import logging
import asyncio
from aiohttp import web
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

# --- الإعدادات (ضع توكن بوتك هنا) ---
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8650385840:AAGVHWVbQ0MzirtA_l6-S83HNKL1O7Jrk2g")
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
       "Dear Instagram / Meta Support Team,\n\n"
"I hope this message finds you well.\n\n"
"My name is [Full Name exactly as in Passport/ID]. I am writing to respectfully appeal the decision to disable my Instagram account.\n\n"
"I recently discovered that my account had been disabled when I attempted to log in. This came as a surprise, as I have always used Instagram responsibly and in full compliance with the Community Guidelines and Terms of Service. To the best of my knowledge, I have not posted any content that violates your policies, nor have I engaged in prohibited activities such as spam, impersonation, harassment, or any form of misuse.\n\n"
"This account is very important to me. It contains years of personal memories, including photos, videos, and meaningful connections with friends and family. Losing access has caused significant inconvenience, and I kindly ask that your team conduct a thorough manual review of the account and reconsider the disablement decision.\n\n"
"I understand that automated systems may sometimes flag accounts incorrectly, and I believe this could be one of those cases. I want to assure you that I remain fully committed to following all of Instagram’s rules and guidelines.\n\n"
"To assist with the verification process, I am ready and willing to provide any required information, including:\n"
"• A clear video selfie for identity confirmation\n"
"• A copy of my government-issued identification (passport or national ID)\n"
"• Any additional details needed to confirm ownership of the account\n\n"
"The account has been consistently accessed from my usual devices and normal usage patterns, without any prior issues.\n\n"
"Thank you sincerely for your time and consideration. I truly value the Instagram community and would greatly appreciate your assistance in restoring access to my account as soon as possible.\n\n"
"Best regards,\n"
"[Full Name]\n"
"Username: [Your Username]\n"
"Email address associated with the account: [Email]\n"
"Phone number (if associated): [Phone Number]"
    )
    await callback.message.answer(full_msg_en)
    await callback.answer()

@dp.callback_query(F.data == "msg_ar")
async def show_msg_ar(callback: types.CallbackQuery):
    full_msg_ar = (
       فريق دعم إنستقرام المحترم،\n\n"
"تحية طيبة وبعد،\n\n"
"أتقدم إليكم بهذا الطلب راجيًا مراجعة حالة حساب تم تعطيله مؤخرًا، حيث أعتقد أن هذا الإجراء قد تم عن طريق الخطأ أو نتيجة سوء فهم. لقد تم استخدام الحساب دائمًا بما يتوافق مع إرشادات مجتمع إنستقرام وشروط الاستخدام، ولم يتم ارتكاب أي مخالفات بشكل متعمد.\n\n"
"طوال فترة استخدام الحساب، كان النشاط طبيعيًا وحقيقيًا، ولم يتم استخدام أي وسائل غير مشروعة مثل الرسائل المزعجة (Spam) أو الأنظمة الآلية أو انتحال الشخصية أو أي سلوك مضلل أو ضار. كما أن جميع المحتويات التي تم نشرها كانت ملتزمة بالسياسات العامة، وخالية من أي مواد مخالفة أو غير لائقة.\n\n"
"قد يكون التعطيل ناتجًا عن نظام آلي أو تفسير خاطئ لبعض الأنشطة، ولذلك أرجو منكم التكرم بإجراء مراجعة يدوية دقيقة للحساب للتأكد من الوضع بشكل عادل. أنا أقدّر جهودكم في الحفاظ على بيئة آمنة وموثوقة، وأحرص بشكل كامل على الالتزام بجميع القوانين والسياسات الخاصة بالمنصة.\n\n"
"في حال وجود أي ملاحظات أو أسباب محددة أدت إلى تعطيل الحساب، أرجو تزويدي بها حتى أتمكن من فهم المشكلة ومعالجتها بالشكل الصحيح. كما أنني مستعد للتعاون وتقديم أي معلومات إضافية قد تساعد في تسهيل عملية المراجعة.\n\n"
"بناءً على ما سبق، أرجو منكم إعادة النظر في القرار وإعادة تفعيل الحساب في أقرب وقت ممكن.\n\n"
"شاكرين لكم وقتكم وتفهمكم ودعمكم.\n\n"
"وتفضلوا بقبول فائق الاحترام والتقدير،\n\n"
"مستخدم مهتم\n\n"
"اسم المستخدم: [your_username]\n"
"البريد الإلكتروني: [your_email@example.com]"
    )
    await callback.message.answer(full_msg_ar)
    await callback.answer()

# --- Minimal health check HTTP server ---
async def health_handler(request):
    return web.Response(text="OK", status=200)

async def run_health_server():
    port = int(os.environ.get("PORT", "8000"))
    app = web.Application()
    app.router.add_get("/", health_handler)
    app.router.add_get("/health", health_handler)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    logging.info(f"Health server running on port {port}")

# --- Main ---
async def main():
    logging.basicConfig(level=logging.INFO)
    print("--- Bot is Running with Paid Service Feature ---")
    # Start health check HTTP server concurrently
    await run_health_server()
    # Delete any active webhook before starting long-polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass
