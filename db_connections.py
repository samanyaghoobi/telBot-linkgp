import mysql.connector # type: ignore
from config import *
#########################################################
#? tables 

#* reservation
def create_reservation_table():
    """
    reservation (id,approved,amount,username,user_id,record_data,record_time)
    Like (1,true or false,15,saaman_pc,1054820423,2024-08-01,"13:00")
    """
    sql=f"""create table reservation(
    id INT AUTO_INCREMENT PRIMARY KEY,
    approved bool NOT NULl DEFAULT 0,
    amount DECIMAL(10,2) NOT NULl,
    user_name VARCHAR(255) NOT NULL, 
    user_id VARCHAR(255) NOT NULL,
    record_date DATE NOT NULL,
    record_time TIME NOT NULl
);"""
    try:
        with mysql.connector.connect(**DB_CONFIG) as connection:
                    with connection.cursor()  as cursor:
                        cursor.execute(sql)
                        connection.commit()
        return True
    except:
         return False
    

#* users
def create_reservation_users():
    """
    users (userid,balance,score,username)
    users (1054820423,10,5,saaman_pc)
    """
    sql=f"""CREATE TABLE users (
    userid BIGINT NOT NULL PRIMARY KEY,
    balance INT DEFAULT 0,
    score INT DEFAULT 0,
    id VARCHAR(255) NOT NULL
)"""
    try:
        with mysql.connector.connect(**DB_CONFIG) as connection:
                    with connection.cursor()  as cursor:
                        cursor.execute(sql)
                        connection.commit()
        return True
    except:
         return False
#* channel_timing
def create_reservation_channel_timing():
    """
    channel_timing see what is it
    """
    sql=f"""create table channel_timing(
 	record_date DATE PRIMARY KEY NOT NULL ,
     hour_13 BOOLEAN NOT NULL DEFAULT 0,
     hour_14 BOOLEAN NOT NULL DEFAULT 0,
     hour_15 BOOLEAN NOT NULL DEFAULT 0,
     hour_16 BOOLEAN NOT NULL DEFAULT 0,
     hour_17 BOOLEAN NOT NULL DEFAULT 0,
     hour_18 BOOLEAN NOT NULL DEFAULT 0,
     hour_18_30 BOOLEAN NOT NULL DEFAULT 0,
     hour_19 BOOLEAN NOT NULL DEFAULT 0,
     hour_19_30 BOOLEAN NOT NULL DEFAULT 0,
     hour_20 BOOLEAN NOT NULL DEFAULT 0,
     hour_20_30 BOOLEAN NOT NULL DEFAULT 0,
     hour_21 BOOLEAN NOT NULL DEFAULT 0,
     hour_21_30 BOOLEAN NOT NULL DEFAULT 0,
     hour_22 BOOLEAN NOT NULL DEFAULT 0,
     hour_22_30 BOOLEAN NOT NULL DEFAULT 0,
     hour_23 BOOLEAN NOT NULL DEFAULT 0,
     hour_23_30 BOOLEAN NOT NULL DEFAULT 0,
     hour_24 BOOLEAN NOT NULL DEFAULT 0,
     hour_24_30 BOOLEAN NOT NULL DEFAULT 0,
     hour_1 BOOLEAN NOT NULL DEFAULT 0,
     hour_1_30 BOOLEAN NOT NULL DEFAULT 0,
     hour_2 BOOLEAN NOT NULL DEFAULT 0);"""
    try:
        with mysql.connector.connect(**DB_CONFIG) as connection:
                    with connection.cursor()  as cursor:
                        cursor.execute(sql)
                        connection.commit()
        return True
    except:
         return False

#########################################################
#! reservation 
#########################################################
def get_all_reservations():
     sql=f"SELECT * FROM reservation;"
     with mysql.connector.connect(**DB_CONFIG) as connection:
          with connection.cursor()  as cursor:
            cursor.execute(sql)
            result =cursor.fetchall()
            return result
#########################################################
def get_reservations_of_month(year,month):
     sql=f"""SELECT *
FROM reservation
WHERE YEAR(record_date) = '{year}' AND MONTH(record_date) = '{month}';
"""
     with mysql.connector.connect(**DB_CONFIG) as connection:
          with connection.cursor()  as cursor:
            cursor.execute(sql)
            result =cursor.fetchall()
            return result

#########################################################
def approve_a_reserve(id):
    sql=f"""UPDATE reservation
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
def update_amount(id,amount):
    sql=f"""UPDATE reservation
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
def add_reserve(amount,user_name,user_id,record_date,record_time):
    sql=f"""INSERT INTO reservation (approved, amount, user_name, user_id, record_date, record_time)
VALUES (0, {amount}, '{user_name}', '{user_id}', '{record_date}', '{record_time}');
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
#! users
########################################################################
def create_user(userid,username):
     try:
        with mysql.connector.connect(**DB_CONFIG) as connection:
            with connection.cursor()  as cursor:
                sql= f"INSERT INTO users(userid,username) VALUES ({userid},'{username}')"
                cursor.execute(sql)
                connection.commit()
                return True
     except:    
          return False
     
##################################################
def get_user(user_id):
     sql=f"""SELECT * FROM users 
     WHERE userid= {user_id};"""
     with mysql.connector.connect(**DB_CONFIG) as connection:
          with connection.cursor()  as cursor:
               cursor.execute(sql)
               result =cursor.fetchone()
     return result
##################################################
def get_all_users():
     sql=f"SELECT * FROM users;"
     with mysql.connector.connect(**DB_CONFIG) as connection:
          with connection.cursor()  as cursor:
            cursor.execute(sql)
            result =cursor.fetchall()
            return result
##################################################
##################################################

def get_user_balance(user_id):
    sql= f"SELECT balance from users where userid = {user_id}"
    with mysql.connector.connect(**DB_CONFIG) as connection:
          with connection.cursor()  as cursor:
               cursor.execute(sql)
               result =cursor.fetchone()
    return result
     
########################################################################
def get_user_score(user_id):
    sql= f"SELECT score from users where userid = {user_id}"
    with mysql.connector.connect(**DB_CONFIG) as connection:
          with connection.cursor()  as cursor:
               cursor.execute(sql)
               result =cursor.fetchone()
    return result
########################################################################
def get_user_id(user_id):
    sql= f"SELECT id from users where userid = {user_id}"
    with mysql.connector.connect(**DB_CONFIG) as connection:
          with connection.cursor()  as cursor:
               cursor.execute(sql)
               result =cursor.fetchone()
    return result
     
########################################################################
def increase_balance(user_id,increase_amount):
    sql= f"UPDATE users SET balance = balance + {increase_amount} WHERE userid = {user_id};"
    with mysql.connector.connect(**DB_CONFIG) as connection:
          with connection.cursor()  as cursor:
               cursor.execute(sql)
               connection.commit()
########################################################################
def decrease_balance(user_id,decrease_balance_amount):
    user_balance=get_user_balance(user_id=user_id)
    if user_balance<decrease_balance_amount :
        return False
    sql= f"UPDATE users SET balance = balance - {decrease_balance_amount} WHERE userid = {user_id};"
    with mysql.connector.connect(**DB_CONFIG) as connection:
          with connection.cursor()  as cursor:
               cursor.execute(sql)
               connection.commit()

    return True
########################################################################
def increase_score(user_id,increase_amount):
    sql= f"UPDATE users SET score = score + {increase_amount} WHERE userid = {user_id};"
    with mysql.connector.connect(**DB_CONFIG) as connection:
          with connection.cursor()  as cursor:
               cursor.execute(sql)
               result =cursor.fetchone()
               connection.commit()
    return result
########################################################################
def decrease_score(user_id,decrease_amount):
    user_score=get_user_score(user_id=user_id)
    if user_score<decrease_amount :
        return False
    sql= f"UPDATE users SET score = score + {decrease_amount} WHERE userid = {user_id};"
    with mysql.connector.connect(**DB_CONFIG) as connection:
          with connection.cursor()  as cursor:
               cursor.execute(sql)
               connection.commit()

    return True
#!#########################################################################