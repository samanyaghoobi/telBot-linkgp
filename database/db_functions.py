import logging
import mysql.connector # type: ignore
from mysql.connector import Error

from configs.auth import DB_CONFIG
from configs.config import db_hour_name,time_of_day
###
#! 
def make_reserve_transaction(user_id,price,time_index,date,banner,link):
    try:
        with mysql.connector.connect(**DB_CONFIG) as connection:
            if connection.is_connected():
                with connection.cursor()  as cursor:

                    connection.start_transaction()
                    sql_decease_balance= f"UPDATE users SET balance = balance - {price} WHERE userid = {user_id};"
                    cursor.execute(sql_decease_balance)

                    time_name=db_hour_name[time_index]
                    sql_set_time=f"""UPDATE channel_timing SET hour_{time_name} = 1 WHERE record_date = '{date}';"""
                    cursor.execute(sql_set_time)

                    time=time_of_day[time_index]
                    sql_make_reserve=f"""INSERT INTO reserve (approved, userid, price, date, time, time_index, banner, link) VALUES (0, {user_id}, {price}, '{date}', '{time}', {time_index}, '{banner}', '{link}');"""
                    cursor.execute(sql_make_reserve)
                    connection.commit()

                    logging.info(" Transaction committed successfully ")

    except Error as e:
        connection.rollback()
        logging.error(f" Error occurred, rolling back: {e} ")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
##############################################################333
def admin_deny_banner(user_id,price,time_index,date,reserve_id):
    try:
        with mysql.connector.connect(**DB_CONFIG) as connection:
            if connection.is_connected():
                with connection.cursor()  as cursor:

                    connection.start_transaction()
                    sql_decease_balance= f"UPDATE users SET balance = balance + {price} WHERE userid = {user_id};"
                    cursor.execute(sql_decease_balance)

                    time_name=db_hour_name[time_index]
                    sql_free_time=f"""UPDATE channel_timing SET hour_{time_name} = 0 WHERE record_date = '{date}';"""
                    cursor.execute(sql_free_time)

                    sql_delete_reserve=f"""DELETE FROM reserve WHERE id = {reserve_id};"""
                    cursor.execute(sql_delete_reserve)
                    connection.commit()

                    logging.info(" Transaction committed successfully")
    except Error as e:
        connection.rollback()
        logging.error(f" Error occurred, rolling back: {e} ")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
##############################################################333
def admin_accept_banner(user_id,time_index,date,reserve_id):
    try:
        with mysql.connector.connect(**DB_CONFIG) as connection:
            if connection.is_connected():
                with connection.cursor()  as cursor:

                    connection.start_transaction()
                    time_name=db_hour_name[time_index]
                    sql_set_time=f"""UPDATE channel_timing SET hour_{time_name} = {user_id} WHERE record_date = '{date}';"""
                    cursor.execute(sql_set_time)

                    sql_approve_reserve=f"""UPDATE reserve SET approved = 1 WHERE id = {reserve_id};"""
                    cursor.execute(sql_approve_reserve)
                    connection.commit()

                    logging.info(" Transaction committed successfully")
    except Error as e:
        connection.rollback()
        logging.error(f" Error occurred, rolling back:  {e} ")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()