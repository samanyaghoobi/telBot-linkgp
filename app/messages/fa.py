from telebot.types import BotCommand
MESSAGES = {
    # General
    "start.welcome"   : "👋 سلام! به ربات خوش آمدی.",
    "admin.panel"     : "📊 خوش آمدی به پنل ادمین.",
    "error.not_member": "❗️ برای استفاده از ربات باید عضو کانال {channel} باشی.",
    "btn.noOption"    : "هیچ گزینه ای وجود ندارد",

    # User buttons
    "btn.user.free_times"     : "🕒 ساعت‌های خالی",
    "btn.user.my_reservations": "📆 مشاهده رزروها",
    "btn.user.convert_points" : "🎁 تبدیل امتیاز",
    "btn.user.profile"        : "👤 حساب کاربری",
    "btn.user.see_banners"    : "🖼 مشاهده بنرها",
    "btn.user.make_banner"    : "🖼 ساخت بنر",
    "btn.user.support"        : "📞 پشتیبانی",
    "btn.user.rules"          : "📜 قوانین و توضیحات",

    # Admin Buttons
    "btn.admin.bot_setting": "⚙️ تنظیمات ربات",
    "btn.admin.reservation": "📆 مدیریت رزروها",
    "btn.admin.user_list"  : "👥 لیست کاربران",
    "btn.admin.income"     : "💰 درآمد",
    "btn.admin.get_backup" : "🗂️ فایل پشتیبان پایگاه داده",
    "btn.find_user":"👥یافتن کاربر",
    "btn.admin.add_setting":"اضافه تنظیمات",
    # Admin Messages
    "msg.admin.user_list": "👥 لیست کاربران 👥",
    "msg.admin.setting"  : "⚙️ لیست تنظیمات ⚙️",
    "msg.find_user"      : "🔍 لطفاً نام کاربری یا پیام حساب کاربری شخص مورد نظر را وارد کنید یا آن را ارسال کنید."
,
    #*--------------- user section --------------------
    # User balance message
    "user.charge.instructions": "💳 برای شارژ حساب خود، لطفاً یکی از پلن‌های زیر را انتخاب یا تصویر رسید را ارسال کنید.",
    "user.balanceIncrease"         : "💳 شارژ حساب",
    # "btn.user.show_banners"   : "🖼 مشاهده بنرها",
    "payment.select_plan"     : (
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
    # User Profile messages
    "user.profile": (
        "👤 نام کاربری : <a href='tg://user?id={user_id}'>{username}</a>\n"
        "🆔 شناسه کاربری :<code>{user_id}</code>\n"
        "💵 موجودی : {balance} هزار تومان\n"
        "💯 امتیاز شما: {score}"
    ),

    # user make Banner messages
    "banner.msg.title" : "🍿 لطفاً عنوانی برای بنر خود وارد کنید:",
    "banner.msg.name"  : "📝 لطفاً نام گروه خود را وارد کنید:",
    "banner.msg.member": "👥 تعداد اعضای گروه را وارد کنید (مثلاً 1234):",
    "banner.msg.link"    : "🔗 لینک گروه را وارد کنید (فقط لینک خصوصی مجاز است):",
    "banner.msg.success": "✅ بنر با موفقیت ساخته شد. در ادامه نمایش داده می‌شود:",
    #banner errors
    "error.banner.limit_reached": "❌ شما به حداکثر تعداد مجاز بنر رسیده‌اید.",
    "error.banner.member"       : "⚠️ تعداد اعضا باید عدد باشد. لطفاً دوباره وارد کنید.",
    "error.banner.link"         : "⚠️ لینک وارد شده معتبر نیست. فقط لینک‌های خصوصی یا داخلی قابل قبول هستند.",
    # user score error
    "error.user.notEnoughScore":("❌ شما حداقل امتیاز کافی را ندارد (حداقل {min})❌"),
    "error.user.notEnoughBalance":"❌موجودی حساب شما کافی نیست❌",
    # user rules message
    "rules.acc"          : "✅ متوجه شدم",
    "rules.explain.plans": "📄 توضیح طرح‌ها",
    "rules.explain.rules": "📜 توضیح قوانین",

    #user reservation 
    "user.msg.reserve.confirm": (
    "✅ شما قصد دارید برای روز {selected_date}({weekday}) ساعت {selected_hour} بنر فوق را رزرو کنید:\n\n"
    "🖼 بنر: {banner_title}\n"
    "💰 قیمت: {price} هزار تومان\n"
    "💳 موجودی شما: {balance} هزار تومان\n\n"
    "💰 برای تایید رزرو و کسر موجودی، تایید کنید."
),


    # Other messages
    "error.not.finished"       : "این امکان در حال حاضر دردسترس نیست",
    "line"                 : "--------------------",
    "msg.select_day"           : "📆 لطفاً یک روز را انتخاب کنید:",
    "msg.selectCustomTime"     : "رزرو بازه دلخواه ( مثلا 8 روز)",
    "msg.noFreeTime"           : "❌ هیچ ساعتی آزاد نیست",
    "msg.noBannerFind"         : "شما هیچ بنری ثبت نکرده‌اید.",
    "msg.selectBanner"         : "📋 لطفاً بنری که می‌خواهید برای این زمان انتخاب کنید را انتخاب کنید.",
    "msg.error.failReservation": "❌ رزرو انجام نشد. لطفاً دوباره تلاش کنید.",
    "msg.customReserveDayInput": "📌 چند روز متوالی می‌خواهی رزرو کنی؟ (بین ۳ تا ۳۰ عدد وارد کن)",
    # general error :
    "error.userNotFound":"❌ کاربر یافت نشد.",

}
ADMIN_COMMANDS = [
    BotCommand("start", "شروع مجدد"),
    BotCommand("user", "از دید کاربر"),
]

# متن قوانین و امتیاز (قابل تنظیم از یک فایل یا دیتابیس)
RULES_TEXT = """
📌 <b>قوانین استفاده از ربات:</b>

1. هر لینک تنها یک‌بار در روز مجاز به تبلیغ است.

2. تبلیغ لینک‌های زیر ممنوع و حذف می‌شود:
   - کانال تلگرام
   - محتوای غیراخلاقی
   - فروش کالا
   - لینک‌های اسکم یا مشکوک

3. گزارش باگ همراه با جایزه است ✅

4. لینک‌ها تا زمانی که تلگرام اجازه دهد قابل ویرایش هستند اما تکرار نمی‌شوند.

5. ارسال لینک فقط از طریق ربات و به‌صورت خودکار انجام می‌شود.

6. اگر لینکی ارسال نشد:
   - موضوع را به ادمین گزارش دهید.
   - مبلغ رزرو بازگردانده می‌شود.
   - و ۵۰٪ بیشتر به ربات بازمی‌گردد.

🎁 <b>سیستم امتیازدهی:</b>
- هر رزرو موفق: 1 امتیاز
- 10 امتیاز = 1 رزرو رایگان
- امتیازها قابل فروش یا انتقال نیستند

⚠️ قوانین ممکن است در آینده تغییر کنند.
"""
PLANS="""

🔷 <b>طرح‌های تبلیغاتی:</b>

📌 <b>طرح ۱</b>
- زمان: ۱۳ تا ۱۷
- حداقل نمایش: ۱ ساعت
- 💰 ۸ هزار تومان

📌 <b>طرح ۲</b>
- زمان: ۱۸ تا ۰۱:۳۰
- حداقل نمایش: نیم ساعت
- 💰 ۱۵ هزار تومان

📌 <b>طرح ویژه</b>
- فقط یک لینک در روز
- زمان: ۰۲:۰۰ شب تا ۱۳:۰۰ ظهر روز بعد
- 💰 ۲۵ هزار تومان

"""