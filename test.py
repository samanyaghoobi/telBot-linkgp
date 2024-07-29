
import mysql.connector # type: ignore
from config import *
from telebot import TeleBot

bot =TeleBot(token = TOKEN)
connection = mysql.connector.connect(**DB_CONFIG)
cursor=connection.cursor() 
sql= f"INSERT INTO users(userid) VALUES (12345)"
cursor.execute(sql)
connection.commit()