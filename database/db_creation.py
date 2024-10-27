import logging
import mysql.connector # type: ignore
from mysql.connector import Error
from configs.auth import DB_CONFIG
from configs.basic_info import *
from database.db_functions import db_set_basic_info
#!###################################################
def dbCreateDatabases():
    try:
        logging.info(f"checking tables")
        # create_data_base()

        result= db_create_table_channel_timing()
        if not result:
            return False
        
        result=db_create_table_reserve()
        if not result:
            return False
        
        result= db_create_table_transactions()
        if not result:
            return False
        
        result=db_create_table_users()
        if not result:
            return False
        
        result=db_create_table_bot_info()
        if not result:
            return False
        
        result=db_set_basic_info()
        if not result:
            return False

        logging.info("data base and tables are ok")

    except Error as e:
        logging.error(e)
        return False
#!###################################################
def db_create_data_base():
    sql="CREATE DATABASE IF NOT EXISTS linkGP;"
    try:
        with mysql.connector.connect(**DB_CONFIG) as connection:
            if connection.is_connected():
                with connection.cursor()  as cursor:
                     cursor.execute(sql)
                     connection.commit()
                     cursor.close()
                     connection.close()
    except Error as e:
        logging.error(f"error from create database: {e}")
####################################################
#* transactions : save each payment of each user 
def db_create_table_transactions():
    """
    transactions (id,approved,amount,username,user_id,record_data,record_time)
    Like (1,true or false,15,saaman_pc,1054820423,2024-08-01,"13:00")
    """
    sql=f"""CREATE TABLE IF NOT EXISTS transactions(
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
            if connection.is_connected():
                with connection.cursor()  as cursor:
                     cursor.execute(sql)
                     connection.commit()
                     cursor.close()
                     connection.close()
                     return True

    except Error as e:
        logging.error(f"error from create transactions: {e} ")
        return False
#!###################################################
#* users table: user info table 
def db_create_table_users():
    """
    users (userid,balance,score,username)
    users (1054820423,10,5,saaman_pc)
    """
    sql=f"""CREATE TABLE IF NOT EXISTS users (
    userid BIGINT NOT NULL PRIMARY KEY,
    balance INT DEFAULT 0,
    score INT DEFAULT 0,
    username VARCHAR(255) NOT NULL
)"""
    try:
        with mysql.connector.connect(**DB_CONFIG) as connection:
            if connection.is_connected():
                with connection.cursor()  as cursor:
                     cursor.execute(sql)
                     connection.commit()
                     cursor.close()
                     connection.close()
                     return True

    except Error as e:
        logging.error(f"error from create users: {e}")
        return False
#!###################################################
#* reserve table : make a reservation connected to time date and user and price
def db_create_table_reserve():
    """
    """
    sql=f"""CREATE TABLE IF NOT EXISTS reserve (
    id INT AUTO_INCREMENT PRIMARY KEY,
    approved bool NOT NULl DEFAULT 0,
    userid BIGINT NOT NULL,
    price INT DEFAULT 0,
    date DATE NOT NULL,
    time TIME NOT NULl,
    time_index  int NOT NULL,
    banner TEXT ,
    link VARCHAR(255) not null,
    UNIQUE (time,date,time_index)
);"""
    try:
        with mysql.connector.connect(**DB_CONFIG) as connection:
            if connection.is_connected():
                with connection.cursor()  as cursor:
                     cursor.execute(sql)
                     connection.commit()
                     cursor.close()
                     connection.close()
                     return True
    except Error as e:
        logging.error(f"error from create reserve: {e} ")
        return False

#!###################################################
#* channel_timing : which time is available
def db_create_table_channel_timing():
    """
    channel_timing see what is it
    each hour show userId that's reserved 
    """
    sql=f"""create table IF NOT EXISTS channel_timing(
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
     hour_01 BIGINT NOT NULL DEFAULT 0,
     hour_01_30 BIGINT NOT NULL DEFAULT 0,
     hour_02 BIGINT NOT NULL DEFAULT 0);"""
    try:
        with mysql.connector.connect(**DB_CONFIG) as connection:
            if connection.is_connected():
                with connection.cursor()  as cursor:
                     cursor.execute(sql)
                     connection.commit()
                     cursor.close()
                     connection.close()
                     return True

    except Error as e:
        logging.error(f"error from create channel_timing: {e} ")
        return False
#!###################################################
#* bot_info
def db_create_table_bot_info():
    """
    """
    sql=f"""CREATE TABLE IF NOT EXISTS bot_setting (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULl DEFAULT 0,
    value TEXT);"""
    try:
        with mysql.connector.connect(**DB_CONFIG) as connection:
            if connection.is_connected():
                with connection.cursor()  as cursor:
                     cursor.execute(sql)
                     connection.commit()
                     cursor.close()
                     connection.close()
                     return True
    except Error as e:
        logging.error(f"error from create db_create_table_bot_info: {e} ")
        return False