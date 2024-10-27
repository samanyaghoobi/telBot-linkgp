from database.db_setting import db_info_getValue
from message_and_text.text import *
from message_and_text.bot_messages import *
##############
def make_user_info (username,user_id,balance,score):
     text=f"""👤 نام کاربری : <a href='tg://user?id={user_id}'>{username}</a>
🆔 شناسه کاربری :<code>{user_id}</code>
💵 موجودی : {balance} هزار تومان
💯 امتیاز شما: {score}"""
     return text


def get_pic_receipt_msg(index):
    text=f"""لطفا عکس رسید خود را ارسال کنید
{make_line}
{get_cart_info()}
💵 مبلغ انتخاب شده: {plans[index]} هزار تومان
"""
    return text

def select_plan_msg(index):
     text=f"""{get_cart_info()}
💵 مبلغ انتخاب شده: {plans[index]} هزار تومان
{make_line}
برای ارسال عکس رسید از دکمه زیر استفاده کنید"""
     return text
################################3
def make_change_score_text(score:int,convert_able:int,value:int):
     text=f"""کل امتیاز شما : {score} ✨
امتیاز قابل تبدیل : {convert_able} ♻️ معادل : {value} هزار تومان💵"""
     return text

################################3
def get_cart_info()->str:
     CART_NUMBER=db_info_getValue(name='CART_NUMBER')[0]
     CART_NAME=db_info_getValue(name='CART_NAME')[0]
     CART_BANK=db_info_getValue(name='CART_BANK')[0]
     cart_info_text=f"""💳 شماره کارت : <code>{CART_NUMBER}</code>
     👤 مالک کارت : {CART_NAME} 
     🏦 بانک : {CART_BANK}"""
     return cart_info_text
################################3
def msg_week_msg_reservation_info(time:str,start_date:str,end_date:str,price,user_balance)->str:
     text=f"""<b>مشخصات رزرو هفتگی شما</b>
⏰ساعت انتخاب شده = <u>{time}</u>
📆تاریخ ارسال اولین لینک = <u>{start_date}</u>
📆تاریخ ارسال اخرین لینک = <u>{end_date}</u>
{make_line}
💵 قیمت                = {price} هزار تومان
💰 موجودی حساب = {user_balance} هزار تومان"""
     return text
################################3
def make_reserve_info_text(time,date,day,price,user_balance):
    return f"""
📝 مشخصات پیش فاکتور رزرو شما:
📅 روز     = {day}
📆 تاریخ  = {date} 
⏰ ساعت = {time}
{make_line}
💵 قیمت                = {price} هزار تومان
💰 موجودی حساب = {user_balance} هزار تومان"""
################################3
def msg_create_income_info(income,month)->str:
     text=f""" درامد شما در ماه 
     📆{months[month]} ({month})📆 
     💵 <b>{income}</b> هزار تومان 💵
    """
     return text