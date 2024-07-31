
# import mysql.connector # type: ignore
# from config import *
# from datetime import datetime,timedelta

# # from main import cal_date
# # bot =TeleBot(token = TOKEN)
# connection = mysql.connector.connect(**DB_CONFIG)
# cursor=connection.cursor() 
# # sql= f"INSERT INTO users(userid) VALUES (12345)"
# # cursor.execute(sql)
# # connection.commit()
# def cal_date(days):
#      return (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")
# # print(cal_date(0))
# sql= f"INSERT INTO channel_timeing(record_date) VALUES ('{cal_date(0)}')"
# cursor.execute(sql)
# connection.commit()