from telebot.types import BotCommand
MESSAGES = {
    # General
    "start.welcome": "سلام 👋 به ربات خوش اومدی!",
    "admin.panel": "📊 خوش اومدی به پنل ادمین.",
    "error.not_member": "❗️برای استفاده از ربات باید عضو کانال {channel} باشی.",
    "btn.noOption":"هیچ گزینه ای وجود ندارد",
    # User buttons
    "btn.free_times": "🕒 ساعت‌های خالی",
    "btn.my_reservations": "📆 مشاهده رزروها",
    "btn.convert_points": "🎁 تبدیل امتیاز",
    "btn.profile": "👤 حساب کاربری",
    "btn.banner": "🖼 ساخت بنر",
    "btn.support": "📞 پشتیبانی",

    # Admin Buttons 
    "btn.admin.bot_setting": "⚙️ تنظیمات ربات",
    "btn.admin.free_time": "📆 مدیریت رزروها",
    "btn.admin.user_list": "👥 لیست کاربران",
    "btn.admin.income": "💰 درآمد",

    "msg.admin.user_list":"👥 لیست کاربران 👥",
    "msg.admin.setting":"⚙️لیست تنظیمات⚙️",
    # "btn.admin.send_msg_to_all":"",



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

    
}
ADMIN_COMMANDS = [
    BotCommand("start", "شروع مجدد"),
    BotCommand("user", "از دید کاربر"),
]