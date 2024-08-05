from config import *

new_user_text='خوش آمدی شما یک کاربر جدید هستید'
old_user_text='سلام کاربر قدیمی'

not_join_text=f'برای استفاده از این ربات باید در کانال ما عضو شوید \n @linkGP'
link = f"https://t.me/{BOT_USERNAME}?start=start"
joined_text="""عضویت شما تایید شد 
لطفا مجدد ربات را راه اندازی کنید 
برای راه اندازی روی 
<a href='{link}'>/start</a>
 ضربه کنید
"""
reboot_text="""مشکلی پیش امده است
لطفا مجدد ربات را راه اندازی کنید 
برای راه اندازی روی 
<a href='{link}'>/start</a>
 ضربه کنید
"""

user_acc_btn="حساب کاربری"
balance_inc_btn='شارژ حساب'
free_rime_btn='ساعت های خالی'
support_btn='پشتیبانی'
support_text="""دقت کنید برای رزو وقت فقط از همین ربات قابل انجام است
جهت ارتباط با پشتیبان به @linkgp_admin پیام دهید"""

back_btn="برگشت به منوی اصلی"
back_btn_msg="به منوی اولیه خوش امدید"

balance_inc_msg="برای افزایش موجودی خود دو راه کار وجود دارد"

### admin btn
admin_btn_user_list="user_list"
admin_btn_send_msg_to_all="send msg to all users"
admin_btn_check_income="check income"
admin_btn_accept_income="accept incomes"
not_admin_text="شما دسترسی ادمین ندارید"

check_income_msg="از لیست زیر ماه میلادی که میخواهید درامد ان را مشاهده کنید انتخاب کنید"
restart_msg="ربات مجدد راه اندازی شد"
check_reservations_text="مشاهده لیست رزرو شده ها"
#?###########################33
increase_balance_msg_final=f"""برای واریز هزینه لطفا از شماره کارت زیر استفاده کنید
<code>{CART_NUMBER}</code>
به نام {CART_NAME}
(با کلیک کردن روی شماره به صورت خودکار کپی میشود)
"""
increase_balance_msg=f"""برای افزایش موجودی لطفا یکی از گزینه های زیر را انتخاب کنید
-------------------------
با شارژ حساب عادی , حساب شما امتیاز دریافت میکند که میتوانید امتیاز هارا خرج کنید
-------------------------
با انتخاب طرح های ویژه شما شامل تخفیف میشوید 
ویژه یک: با پرداخت {price_plan1_off} هزار تومان حساب شما {price_plan1} هزار تومان شارژ میشود
ویژه دو: با پرداخت {price_plan2_off} هراز تومان حساب شما {price_plan2} هزار تومان شارژ میشود
ویژه سه: با پرداخت {price_plan3_off} هزار تومان حساب شما {price_plan3} هزار تومان شارژ میشود
-------------------------
"""
increase_plans=[f"{price_1} هزار تومان (یک امتیاز)",f"{price_2} هزار تومان (دو امتیاز)",f"{price_3} هزار تومان(سه امتیاز)",
                f"ویژه یک=>{price_plan1_off} هزار تومان ",f"ویژه دو=>{price_plan2_off} هزار تومان ",f"ویژه سه=>{price_plan3_off} هزار تومان "]
                
admin_welcome_msg="خوش امدی ادمین"