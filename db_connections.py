import mysql.connector # type: ignore
from config import *

#########################################################
#? tables 

#* balance
def create_table_transactions():
    """
    transactions (id,approved,amount,username,user_id,record_data,record_time)
    Like (1,true or false,15,saaman_pc,1054820423,2024-08-01,"13:00")
    """
    sql=f"""create table transactions(
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
    

#* users table
def create_table_users():
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
#* reserve table
def create_table_reserve():
    """
    """
    sql=f"""CREATE TABLE reserve (
    id INT AUTO_INCREMENT PRIMARY KEY,
    approved bool NOT NULl DEFAULT 0,
    userid BIGINT NOT NULL,
    price INT DEFAULT 0,
    date DATE NOT NULL,
    time TIME NOT NULl,
    time_index  int NOT NULL,
    banner TEXT ,
    link VARCHAR(255) not null
);"""
    try:
        with mysql.connector.connect(**DB_CONFIG) as connection:
                    with connection.cursor()  as cursor:
                        cursor.execute(sql)
                        connection.commit()
        return True
    except:
         return False
#* channel_timing
def create_table_channel_timing():
    """
    channel_timing see what is it
    each hour show userId that's reserved 
    """
    sql=f"""create table channel_timing(
 	record_date DATE PRIMARY KEY NOT NULL ,
     hour_13 BIGINT NOT NULL DEFAULT 0,
     hour_14 BIGINT NOT NULL DEFAULT 0,
     hour_15 BIGINT NOT NULL DEFAULT 0,
     hour_16 BIGINT NOT NULL DEFAULT 0,
     hour_17 BIGINT NOT NULL DEFAULT 0,
     hour_18 BIGINT NOT NULL DEFAULT 0,
     hour_18_30 BIGINT NOT NULL DEFAULT 0,
     hour_19 BIGINT NOT NULL DEFAULT 0,
     hour_19_30 BIGINT NOT NULL DEFAULT 0,
     hour_20 BIGINT NOT NULL DEFAULT 0,
     hour_20_30 BIGINT NOT NULL DEFAULT 0,
     hour_21 BIGINT NOT NULL DEFAULT 0,
     hour_21_30 BIGINT NOT NULL DEFAULT 0,
     hour_22 BIGINT NOT NULL DEFAULT 0,
     hour_22_30 BIGINT NOT NULL DEFAULT 0,
     hour_23 BIGINT NOT NULL DEFAULT 0,
     hour_23_30 BIGINT NOT NULL DEFAULT 0,
     hour_24 BIGINT NOT NULL DEFAULT 0,
     hour_24_30 BIGINT NOT NULL DEFAULT 0,
     hour_1 BIGINT NOT NULL DEFAULT 0,
     hour_1_30 BIGINT NOT NULL DEFAULT 0,
     hour_2 BIGINT NOT NULL DEFAULT 0);"""
    try:
        with mysql.connector.connect(**DB_CONFIG) as connection:
                    with connection.cursor()  as cursor:
                        cursor.execute(sql)
                        connection.commit()
        return True
    except:
         return False

#########################################################
#! reserve table 
#########################################################
#*add :save : create
def make_a_reservation(userid,price,date,time,time_index,banner,link):
    sql=f"""INSERT INTO reserve (approved, userid, price, date, time, time_index, banner, link)
VALUES (0, {userid}, {price}, '{date}', '{time}', {time_index}, '{banner}', '{link}');
"""
    print(sql)
    try:
        with mysql.connector.connect(**DB_CONFIG) as connection:
                    with connection.cursor()  as cursor:
                       result= cursor.execute(sql)
                       print(result)
                       connection.commit()
        return True
    except:
         return False
#*approve
def approve_a_reserve(id):
    sql=f"""UPDATE reserve
SET approved = 1
WHERE id = {id};
"""
    try:
        with mysql.connector.connect(**DB_CONFIG) as connection:
                    with connection.cursor()  as cursor:
                        cursor.execute(sql)
                        connection.commit()
        return True
    except:
         return False
#*get banner_with id
def get_banner_with_id_reserve(id):
     sql=f"""SELECT banner
FROM reserve
WHERE id = {id};
"""
     with mysql.connector.connect(**DB_CONFIG) as connection:
          with connection.cursor()  as cursor:
            cursor.execute(sql)
            result =cursor.fetchone()
            return result
#* get id with time and date
def get_id_with_time_date_reserve(time,date):
     sql=f"""SELECT id 
FROM reserve 
WHERE date = '{date}' AND time = '{time}';

"""
     with mysql.connector.connect(**DB_CONFIG) as connection:
          with connection.cursor()  as cursor:
            cursor.execute(sql)
            result =cursor.fetchone()
            return result

#* get link with id 
def get_link_with_id_reserve(id):
     sql=f"""SELECT link
FROM reserve
WHERE id = {id};
"""
     with mysql.connector.connect(**DB_CONFIG) as connection:
          with connection.cursor()  as cursor:
            cursor.execute(sql)
            result =cursor.fetchone()
            return result


#* get links of day with date 
def get_link_with_id_reserve(date):
     sql=f"""SELECT link 
FROM reserve 
WHERE date = '{date}';
"""
     with mysql.connector.connect(**DB_CONFIG) as connection:
          with connection.cursor()  as cursor:
            cursor.execute(sql)
            result =cursor.fetchall()
            return result

#* get  all 
def get_all_reserves():
     sql=f"SELECT * FROM reserve;"
     with mysql.connector.connect(**DB_CONFIG) as connection:
          with connection.cursor()  as cursor:
            cursor.execute(sql)
            result =cursor.fetchall()
            return result
#########################################################
#! transactions 
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
##########################################################################
#! channel timing
def create_channel_timing(day):
    sql= f"INSERT INTO channel_timing(record_date) VALUES ('{day}');"
    try:
            with mysql.connector.connect(**DB_CONFIG) as connection:
              with connection.cursor()  as cursor:
                cursor.execute(sql)
                connection.commit()
            return True
    except:
           return False

def update_channel_timing(time_index,userid,date):
    time=db_hour_name[time_index]
    sql=f"""UPDATE channel_timing
SET hour_{time} = {userid}
WHERE record_date = '{date}';"""
    try:
            with mysql.connector.connect(**DB_CONFIG) as connection:
              with connection.cursor()  as cursor:
                cursor.execute(sql)
                connection.commit()
            return True
    except:
           return False
    
