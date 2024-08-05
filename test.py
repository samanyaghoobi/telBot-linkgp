
import mysql.connector # type: ignore
from config import *
from datetime import datetime,timedelta
# from custom_functions import *
from custom_functions import compare_time, is_banner_ok
from db_connections import create_table_transactions
# # from main import cal_date
# # bot =TeleBot(token = TOKEN)
# connection = mysql.connector.connect(**DB_CONFIG)
# cursor=connection.cursor() 
# # sql= f"INSERT INTO users(userid) VALUES (12345)"
# # cursor.execute(sql)
# # connection.commit()
# # sql= f"UPDATE users SET balance = balance + {10} WHERE userid = {123};"
# sql= f"UPDATE users SET balance = balance - {30} WHERE userid = {123};"

# cursor.execute(sql)
# connection.commit()
# result =cursor.fetchone()
# print(res)
# def get_all_users():
#      sql=f"SELECT * FROM users;"
#      with mysql.connector.connect(**DB_CONFIG) as connection:
#           with connection.cursor()  as cursor:
#             cursor.execute(sql)
#             result =cursor.fetchall()
#             return result

# result =get_all_users()
# for user in result:
#     print (user)
# name="123"
# member="123"
# description="123"
# link="123"
# banner= make_channel_banner(name=name,members=member,description=description,link=link)
# print(banner)
# for i in range(len(time_of_day)):
#     print(time_of_day[i])

# result=get_user(user_id="5416152450")
# print (result is not None)

# create_reservation_channel_timing()
# print(cal_date(0))
# update_channel_timing(time_index=2,userid=12431234123,date="2024-08-05")
# create_table_transactions()
# add_transactions(amount=123123,user_id=12312312,user_name=call.from_user.username,record_date=current_date(),record_time=get_current_time())


# result =compare_time(time1="23:50",time2="00:00")
# print(result)
text = """Super GP

naмe : GroupName

мeмвer: 123

𝓭𝓮𝓼𝓬𝓻𝓲𝓹𝓽𝓲𝓸𝓷: A description of the group.

lιnĸ: http://example.com

@LinkGP



"""

if is_banner_ok(text):
    print("yes")
else:
    print("no")