from configs.auth import BOT_USERNAME
from configs.basic_info import *
from message_and_text.bot_messages import make_line
msg_start_command=f"""🥳خوش امدید🥳
این ربات مخصوص کانال @linkGp است
{make_line}
مراحل استفاده از ربات:
۱. ابتدا حساب کاربری خود را شارژ کنید💵
۲. منتظر تایید ادمین بمانید⏳
۳. سپس یک بنر برای خود بسازید📝
۴. از بخش 'ساعت های خالی' ساعت مورد نظر رو انتخاب کنید⏰
"""

admin_link=""
not_join_text=f'برای استفاده از این ربات باید در کانال ما عضو شوید \n @linkGP'
restart_link_bot = f"https://t.me/{BOT_USERNAME}?start=start"

reboot_text="""مشکلی پیش امده است
لطفا مجدد ربات را راه اندازی کنید 
برای راه اندازی روی 
<a href='{link}'>/start</a>
 ضربه کنید
"""
markup_user_find_reserve="✅مشاهده  رزرو ها"
markup_user_account_btn="👤 حساب کاربری"
balance_inc_btn='شارژ حساب'
markup_user_free_rime='⏰ ساعت های خالی'
markup_user_make_banner='📝 ساخت بنر'
btn_support='🆘 پشتیبانی'
btn_convert_score='✨تبدیل امتیاز'

back_btn="برگشت به منوی اصلی"
back_btn_msg="به منوی اولیه خوش امدید"

balance_inc_msg="برای افزایش موجودی خود دو راه کار وجود دارد"

#! admin btn
#mains
admin_btn_user_list="👤لیست کاربر ها"
admin_btn_find_user_info="👤پیدا کردن کاربر👤"
admin_btn_bot_setting="تنظیمات ربات🤖"
admin_btn_send_msg_to_all="ارسال پیام عمومی✍🏻"
admin_btn_check_income="محاسبه درامد💰"
admin_btn_reserves="مشاهده رزرو ها✅"
not_admin_text="شما دسترسی ادمین ندارید"

#
check_reservations_text="مشاهده لیست رزرو شده ها"

admin_btn_increase_score='افزایش امتیاز کاربر'
admin_btn_increase_balance='افزایش موجودی کاربر'
admin_btn_decrease_score='کاهش امتیاز کاربر'
admin_btn_decrease_balance='کاهش موجودی کاربر'
admin_btn_delete_user='پاک کردن کاربر'
admin_btn_msg_user='ارسال پیام به کاربر'

admin_btn_cancel_reserve='کنسل کردن رزرو'
admin_btn_change_banner='تغییر بنر'
#?###########################33
#markup for bot setting
admin_btn_bot_setting_change_cart="تغییر شماره کارت"
admin_btn_bot_setting_change_price="تغییر قیمت"
admin_btn_restart_bot="راه اندازی مجدد ربات"
msg_card_number_is_not_valid="شماره کارت وارد شده صحیح نیست دوباره تلاش کنید"
#?###########################33


increase_plans_btn_text=[f"{price_1} هزار تومان (یک امتیاز)",
                         f"{price_2} هزار تومان (دو امتیاز)",
                         f"{price_3} هزار تومان(سه امتیاز)",
                        f"ویژه یک: {price_plan1_off} هزار تومان ",
                        f"ویژه دو: {price_plan2_off} هزار تومان ",
                        f"ویژه سه: {price_plan3_off} هزار تومان "]
                
admin_welcome_msg="خوش امدی ادمین"

forward_banner_text="بنر شما برای ادمین ارسال شد \n پس از تایید لینک به صورت خودکار ارسال میشود"
accept_banner_text="بنر شما برای ادمین ارسال شد \n پس از تایید لینک به صورت خودکار ارسال میشود"
##############3
msg_banner_not_mach=f"""🚫بنر ارسالی شما با الگوی کانال همخوانی ندارد🚫
لطفا از دکمه '{markup_user_make_banner}' استفاده کنید
و مجدد تلاش کنید🙏🏻
"""
########################33
restart_markup_text="/start"

text_bot_is_disable="ربات غیر فعال است لطفا بعدا تلاش کنید"
msg_error_to_user="مشکلی پیش آمده است لطفا دوباره تلاش کنید"