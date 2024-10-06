import logging
import mysql.connector # type: ignore
from mysql.connector import Error
from configs.auth import DB_CONFIG
from configs.basic_info import *


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
        logging.error(f" error get_all_transactions:   {e} ")
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
        logging.error(f" error get_transactions_of_month:   {e} ")
#########################################################
def get_transactions_of_month_approved(year,month):
     sql=f"""SELECT *
FROM transactions
WHERE YEAR(record_date) = '{year}' AND MONTH(record_date) = '{month}' AND  approved = 1;
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
        logging.error(f" error get_transactions_of_month:   {e} ")
#########################################################
def get_transactions_of_month_income(year,month):
     sql=f"""SELECT SUM(amount)
FROM transactions
WHERE YEAR(record_date) = '{year}' AND MONTH(record_date) = '{month}';
"""
     try:
        with mysql.connector.connect(**DB_CONFIG) as connection:
            if connection.is_connected():
                with connection.cursor()  as cursor:
                     cursor.execute(sql)
                    #  connection.commit()
                     income=cursor.fetchone()
                     cursor.close()
                     connection.close()
                     return income[0]
     except Error as e:
        logging.error(f" error get_transactions_of_month:   {e} ")
#########################################################
def get_transactions_of_month_approved_income(year,month):
     sql=f"""SELECT SUM(amount)
FROM transactions
WHERE YEAR(record_date) = '{year}' AND MONTH(record_date) = '{month}' AND  approved = 1;
"""
     try:
        with mysql.connector.connect(**DB_CONFIG) as connection:
            if connection.is_connected():
                with connection.cursor()  as cursor:
                     cursor.execute(sql)
                    #  connection.commit()
                     income=cursor.fetchone()
                     cursor.close()
                     connection.close()
                     return income[0]
     except Error as e:
        logging.error(f" error get_transactions_of_month:   {e} ")
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
        logging.error(f" error approve_a_transactions:   {e} ")
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
        logging.error(f" error update_amount_transactions:   {e} ")
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
        logging.error(f" error add_transactions:    {e} ")
#########################################################
