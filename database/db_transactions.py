import logging
import mysql.connector # type: ignore
from mysql.connector import Error
from configs.auth import DB_CONFIG
from configs.config import *


#########################################################
def get_all_transactions():
     sql=f"SELECT * FROM transactions;"
     try:
        with mysql.connector.connect(**DB_CONFIG) as connection:
            if connection.is_connected():
                with connection.cursor()  as cursor:
                     cursor.execute(sql)
                    #  connection.commit()
                     transactions=cursor.fetchall()
                     cursor.close()
                     connection.close()
                     return transactions

     except Error as e:
        logging.error(f"\033[91merror get_all_transactions: \n {e} \n \033[0m")
#########################################################
def get_transactions_of_month(year,month):
     sql=f"""SELECT *
FROM transactions
WHERE YEAR(record_date) = '{year}' AND MONTH(record_date) = '{month}';
"""
     try:
        with mysql.connector.connect(**DB_CONFIG) as connection:
            if connection.is_connected():
                with connection.cursor()  as cursor:
                     cursor.execute(sql)
                    #  connection.commit()
                     transactions=cursor.fetchall()
                     cursor.close()
                     connection.close()
                     return transactions
     except Error as e:
        logging.error(f"\033[91merror get_transactions_of_month: \n {e} \n \033[0m")
#########################################################
def approve_a_transactions(id):
     sql=f"""UPDATE transactions
SET approved = 1
WHERE id = {id};"""
     try:
        with mysql.connector.connect(**DB_CONFIG) as connection:
            if connection.is_connected():
                with connection.cursor()  as cursor:
                     cursor.execute(sql)
                     connection.commit()
                     cursor.close()
                     connection.close()
     except Error as e:
        logging.error(f"\033[91merror approve_a_transactions: \n {e} \n \033[0m")
#########################################################
def update_amount_transactions(id,amount):
     sql=f"""UPDATE transactions
SET amount = {amount}
WHERE id = {id};"""
     try:
        with mysql.connector.connect(**DB_CONFIG) as connection:
            if connection.is_connected():
                with connection.cursor()  as cursor:
                     cursor.execute(sql)
                     connection.commit()
                     cursor.close()
                     connection.close()
     except Error as e:
        logging.error(f"\033[91merror update_amount_transactions: \n {e} \n \033[0m")
#########################################################
def add_transactions(approve,amount,user_name,user_id,record_date,record_time):
     sql=f"""INSERT INTO transactions (approved, amount, user_name, user_id, record_date, record_time)
VALUES ({approve}, {amount}, '{user_name}', '{user_id}', '{record_date}', '{record_time}');
""" 
     try:
        with mysql.connector.connect(**DB_CONFIG) as connection:
            if connection.is_connected():
                with connection.cursor()  as cursor:
                     cursor.execute(sql)
                     connection.commit()
                     cursor.close()
                     connection.close()
     except Error as e:
        logging.error(f"\033[91merror add_transactions:  \n {e} \n \033[0m")
#########################################################
