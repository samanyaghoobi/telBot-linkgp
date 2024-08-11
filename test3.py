from datetime import datetime
from configs.auth import ADMIN_ID_LIST, CHANNELS_USERNAME
from database.db_reserve import get_banner_with_id_reserve, get_id_with_time_date_reserve
from database.db_timing import check_time_date,update_channel_timing
from functions.custom_functions import find_index, get_current_date
from configs.config import time_of_day  

current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
text = f"این یک پیام زمان‌بندی‌شده است که در {current_time} ارسال شده است."
# bot.send_message(ADMIN_ID_LIST[1], text)
time=datetime.now().strftime('%H:%M')
time='01:00'
time_index=find_index(time,time_of_day)
date=get_current_date()
date='2024-08-17'
time_check=check_time_date(time=time,date=date)
print(time_check)
print('test')
if time_check is not None :
    user_id=int(time_check[0])
    if user_id != 1 :
        reserve_id=get_id_with_time_date_reserve(time=time,date=date)[0]
        print(reserve_id)
        banner=get_banner_with_id_reserve(reserve_id)
        for channel in CHANNELS_USERNAME:
            print(banner)
            # bot.send_message(chat_id=channel,text=banner,disable_web_page_preview=True,link_preview_options=False)
          

# print(result)