from telebot.types import BotCommand
MESSAGES = {
    # General
    "start.welcome"   : "سلام 👋 به ربات خوش اومدی!",
    "admin.panel"     : "📊 خوش اومدی به پنل ادمین.",
    "error.not_member": "❗️برای استفاده از ربات باید عضو کانال {channel} باشی.",
    "btn.noOption"    : "هیچ گزینه ای وجود ندارد",
    # User buttons
    "btn.free_times"      : "🕒 ساعت‌های خالی",
    "btn.my_reservations" : "📆 مشاهده رزروها",
    "btn.convert_points"  : "🎁 تبدیل امتیاز",
    "btn.profile"         : "👤 حساب کاربری",
    "btn.user.make_banner": "🖼 ساخت بنر",
    "btn.support"         : "📞 پشتیبانی",

    # Admin Buttons 
    "btn.admin.bot_setting": "⚙️ تنظیمات ربات",
    "btn.admin.reservation"  : "📆 مدیریت رزروها",
    "btn.admin.user_list"  : "👥 لیست کاربران",
    "btn.admin.income"     : "💰 درآمد",
    "btn.admin.get_backup" : "دریافت فایل پشتیبانی پایگاه داده",

    "msg.admin.user_list"      : "👥 لیست کاربران 👥",
    "msg.admin.setting"        : "⚙️لیست تنظیمات⚙️",
    # "btn.admin.send_msg_to_all": "",
    "user.charge.instructions": "💳 برای شارژ حساب خود، لطفاً یکی از پلن‌های زیر را انتخاب یا تصویر رسید را ارسال کنید.",
    "btn.user.charge":"💳 شارژ حساب",
    "btn.user.show_banners":"🖼 مشاهده بنرها",

    "user.profile": (
        "👤 نام کاربری : <a href='tg://user?id={user_id}'>{username}</a>\n"
        "🆔 شناسه کاربری :<code>{user_id}</code>\n"
        "💵 موجودی : {balance} هزار تومان\n"
        "💯 امتیاز شما: {score}"
    ),

    "payment.select_plan": (
        "{cart_info}\n"
        "💵 مبلغ انتخاب شده: {price} هزار تومان\n"
        "{line}\n"
        "برای ارسال عکس رسید از دکمه زیر استفاده کنید"
    ),

    "payment.upload_receipt": (
        "لطفا عکس رسید خود را ارسال کنید\n"
        "{line}\n"
        "{cart_info}\n"
        "💵 مبلغ انتخاب شده: {price} هزار تومان"
    ),

    "btn.user.make_banner": "🖼 ساخت بنر",
    "prompt.banner.title": "🏷 لطفاً عنوانی برای بنر خود وارد کنید:",

    "prompt.banner.name"  : "📝 لطفاً نام گروه خود را وارد کنید:",
    "prompt.banner.member": "👥 تعداد اعضای گروه را وارد کنید (مثلاً 1234):",
    "prompt.banner.link"  : "🔗 لینک گروه را وارد کنید (فقط لینک خصوصی مجاز است):",

    "error.banner.limit_reached": "❌ شما به حداکثر تعداد مجاز بنر رسیده‌اید.",
    "error.banner.member"       : "⚠️ تعداد اعضا باید عدد باشد. لطفاً دوباره وارد کنید.",
    "error.banner.link"         : "⚠️ لینک وارد شده معتبر نیست. فقط لینک‌های خصوصی یا داخلی قابل قبول هستند.",

    "success.banner.created": "✅ بنر با موفقیت ساخته شد. در ادامه نمایش داده می‌شود:",

    "error.not.finished":"این امکان در حال حاضر دردسترس نیست"
    ,"txt.line":"--------------------"
}
ADMIN_COMMANDS = [
    BotCommand("start", "شروع مجدد"),
    BotCommand("user", "از دید کاربر"),
]