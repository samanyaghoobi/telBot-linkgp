import mysql.connector # type: ignore
from configs.auth import *
from configs.config import *
#!###################################################
def create_all_table():
    try:
        create_table_channel_timing()
        create_table_reserve()
        create_table_transactions()
        create_table_users()
        return True
    except:
          return False
#!###################################################
#* transactions : save each payment of each user 
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
    
#!###################################################
#* users table: user info table 
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
#!###################################################
#* reserve table : make a reservation connected to time date and user and price
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
    

#!###################################################
#* channel_timing : which time is available
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
