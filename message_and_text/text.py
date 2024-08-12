from configs.auth import BOT_USERNAME
from configs.config import *

new_user_text='خوش آمدی شما یک کاربر جدید هستید'
old_user_text='سلام کاربر قدیمی'
admin_link=""
not_join_text=f'برای استفاده از این ربات باید در کانال ما عضو شوید \n @linkGP'
restart_link_bot = f"https://t.me/{BOT_USERNAME}?start=start"

reboot_text="""مشکلی پیش امده است
لطفا مجدد ربات را راه اندازی کنید 
برای راه اندازی روی 
<a href='{link}'>/start</a>
 ضربه کنید
"""

user_acc_btn="👤 حساب کاربری"
balance_inc_btn='شارژ حساب'
free_rime_btn='⏰ ساعت های خالی'
make_banner_btn='📝 ساخت بنر'
support_btn='🆘 پشتیبانی'

back_btn="برگشت به منوی اصلی"
back_btn_msg="به منوی اولیه خوش امدید"

balance_inc_msg="برای افزایش موجودی خود دو راه کار وجود دارد"

### admin btn
admin_btn_user_list="user_list"
admin_btn_find_user_info="find_user_info"
admin_btn_bot_info="bot_info"
admin_btn_send_msg_to_all="send msg to all users"
admin_btn_check_income="check income"
admin_btn_accept_income="accept incomes"
not_admin_text="شما دسترسی ادمین ندارید"

check_income_msg="از لیست زیر ماه میلادی که میخواهید درامد ان را مشاهده کنید انتخاب کنید"
check_reservations_text="مشاهده لیست رزرو شده ها"


admin_btn_increase_score='admin_btn_in_score'
admin_btn_increase_balance='admin_btn_in_balance'
admin_btn_decrease_score='admin_btn_de_score'
admin_btn_decrease_balance='admin_btn_de_balance'
admin_btn_delete_user='delete_user'
admin_btn_msg_user='send_message_to_user'
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
cart_info_text=f"""💳 شماره کارت : <code>{CART_NUMBER}</code>
👤 مالک کارت : {CART_NAME} 
🏦 بانک : {CART_BANK}"""
banner_not_mach=f"""بنر ارسالی شما با الگوی کانال همخوانی ندارد 
لطفا از دکمه '{make_banner_btn}' استفاده کنید
و مجدد تلاش کنید
"""
########################33
restart_markup_text="/start"