import mysql.connector # type: ignore
from configs.config import *


#########################################################
def get_all_transactions():
     sql=f"SELECT * FROM transactions;"
     with mysql.connector.connect(**DB_CONFIG) as connection:
          with connection.cursor()  as cursor:
            cursor.execute(sql)
            result =cursor.fetchall()
            return result
#########################################################
def get_transactions_of_month(year,month):
     sql=f"""SELECT *
FROM transactions
WHERE YEAR(record_date) = '{year}' AND MONTH(record_date) = '{month}';
"""
     with mysql.connector.connect(**DB_CONFIG) as connection:
          with connection.cursor()  as cursor:
            cursor.execute(sql)
            result =cursor.fetchall()
            return result

#########################################################
def approve_a_transactions(id):
    sql=f"""UPDATE transactions
SET approved = 1
WHERE id = {id};"""
    try:
        with mysql.connector.connect(**DB_CONFIG) as connection:
                    with connection.cursor()  as cursor:
                        cursor.execute(sql)
                        connection.commit()
        return True
    except:
         return False
#########################################################
def update_amount_transactions(id,amount):
    sql=f"""UPDATE transactions
SET amount = {amount}
WHERE id = {id};"""
    try:
        with mysql.connector.connect(**DB_CONFIG) as connection:
                    with connection.cursor()  as cursor:
                        cursor.execute(sql)
                        connection.commit()
        return True
    except:
         return False
#########################################################
def add_transactions(approve,amount,user_name,user_id,record_date,record_time):
    sql=f"""INSERT INTO transactions (approved, amount, user_name, user_id, record_date, record_time)
VALUES ({approve}, {amount}, '{user_name}', '{user_id}', '{record_date}', '{record_time}');
""" 
    try:
        with mysql.connector.connect(**DB_CONFIG) as connection:
                    with connection.cursor()  as cursor:
                        cursor.execute(sql)
                        connection.commit()
        return True
    except:
         return False
#########################################################
