import logging
import mysql.connector # type: ignore
from mysql.connector import Error

from configs.auth import DB_CONFIG
from configs.basic_info import db_hour_name,dayClockArray
from database.db_setting import db_info_exist, db_info_getValue, db_info_insert
from functions.calender_functions import cal_date, get_next_day
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

                    time=dayClockArray[time_index]
                    sql_make_reserve=f"""
                    INSERT INTO reserve (approved, userid, price, date, time, time_index, banner, link) VALUES 
                    (0, {user_id}, {price}, '{date}', '{time}', {time_index}, '{banner}', '{link}');"""
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
def make_reserve_transaction_weak_reserve(user_id,price,time_index,start_date,banner,link,approved=1):
    try:
        date0=start_date
        date1=get_next_day(start_date)
        date2=get_next_day(date1)
        date3=get_next_day(date2)
        date4=get_next_day(date3)
        date5=get_next_day(date4)
        date6=get_next_day(date5)

        with mysql.connector.connect(**DB_CONFIG) as connection:
            if connection.is_connected():
                with connection.cursor()  as cursor:

                    connection.start_transaction()
                    sql_decease_balance= f"UPDATE users SET balance = balance - {(price*7)} WHERE userid = {user_id};"
                    cursor.execute(sql_decease_balance)

                    time_name=db_hour_name[time_index]
                    sql_set_time=f"""UPDATE channel_timing
                    SET 
                        hour_{time_name} = CASE record_date
                            WHEN '{date0}' THEN 1
                            WHEN '{date1}' THEN 1
                            WHEN '{date2}' THEN 1
                            WHEN '{date3}' THEN 1
                            WHEN '{date4}' THEN 1
                            WHEN '{date5}' THEN 1
                            WHEN '{date6}' THEN 1
                            ELSE hour_{time_name} 
                        END
                    WHERE record_date IN ('{date0}', '{date1}', '{date2}', '{date3}', '{date4}', '{date5}', '{date6}');
                    """
                    cursor.execute(sql_set_time)

                    time=dayClockArray[time_index]
                    sql_make_reserve=f"""
                    INSERT INTO reserve (approved, userid, price, date, time, time_index, banner, link) VALUES 
                    (1, {user_id}, {price}, '{date0}', '{time}', {time_index}, '{banner}', '{link}'),
                    (1, {user_id}, {price}, '{date1}', '{time}', {time_index}, '{banner}', '{link}'),
                    (1, {user_id}, {price}, '{date2}', '{time}', {time_index}, '{banner}', '{link}'),
                    (1, {user_id}, {price}, '{date3}', '{time}', {time_index}, '{banner}', '{link}'),
                    (1, {user_id}, {price}, '{date4}', '{time}', {time_index}, '{banner}', '{link}'),
                    (1, {user_id}, {price}, '{date5}', '{time}', {time_index}, '{banner}', '{link}'),
                    (1, {user_id}, {price}, '{date6}', '{time}', {time_index}, '{banner}', '{link}');"""
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
def transactions_admin_accept_banner(user_id,time_index,date,reserve_id):
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
##############################################################333
def transactions_admin_accept_banner_weak_reserve(user_id,time_index,start_date,reserve_id):
    date0=start_date
    date1=get_next_day(start_date)
    date2=get_next_day(date1)
    date3=get_next_day(date2)
    date4=get_next_day(date3)
    date5=get_next_day(date4)
    date6=get_next_day(date5)
    try:
        with mysql.connector.connect(**DB_CONFIG) as connection:
            if connection.is_connected():
                with connection.cursor()  as cursor:

                    connection.start_transaction()
                    time_name=db_hour_name[time_index]
                    sql_set_time=f"""UPDATE channel_timing
                    SET 
                        hour_{time_name} = CASE record_date
                            WHEN '{date0}' THEN {user_id}
                            WHEN '{date1}' THEN {user_id}
                            WHEN '{date2}' THEN {user_id}
                            WHEN '{date3}' THEN {user_id}
                            WHEN '{date4}' THEN {user_id}
                            WHEN '{date5}' THEN {user_id}
                            WHEN '{date6}' THEN {user_id}
                            ELSE hour_{time_name} 
                        END
                    WHERE record_date IN ('{date0}', '{date1}', '{date2}', '{date3}', '{date4}', '{date5}', '{date6}');
                    """
                    cursor.execute(sql_set_time)
                    #? temporary
                    # sql_approve_reserve=f"""UPDATE reserve SET approved = 1 WHERE id = {reserve_id};"""
                    # cursor.execute(sql_approve_reserve)
                    connection.commit()

                    logging.info(" Transaction committed successfully")
    except Error as e:
        connection.rollback()
        logging.error(f" Error occurred, rolling back:  {e} ")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
##############################################################333
def db_convert_score(user_id:int,score_to_decrease:int,balance_to_increase:int):
    try:
        with mysql.connector.connect(**DB_CONFIG) as connection:
            if connection.is_connected():
                with connection.cursor()  as cursor:

                    connection.start_transaction()
                    sql_decrease_score= f"UPDATE users SET score = score - {score_to_decrease} WHERE userid = {user_id};"
                    cursor.execute(sql_decrease_score)

                    sql_increase_balance=f"UPDATE users SET balance = balance + {balance_to_increase} WHERE userid = {user_id};"
                    cursor.execute(sql_increase_balance)
                    connection.commit()

                    logging.info(" Transaction committed successfully")
    except Error as e:
        connection.rollback()
        logging.error(f" Error occurred, rolling back - db_convert_score:  {e} ")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
##############################################################333
def db_set_new_cart(number:int,bank_name:int,owner:int):
    try:
        with mysql.connector.connect(**DB_CONFIG) as connection:
            if connection.is_connected():
                with connection.cursor()  as cursor:

                    connection.start_transaction()
                    sql_number= f"UPDATE info SET value = '{number}' WHERE name = 'CART_NUMBER' ;"
                    cursor.execute(sql_number)

                    sql_name= f"UPDATE info SET value = '{owner}' WHERE name = 'CART_NAME' ;"
                    cursor.execute(sql_name)

                    sql_bank_name= f"UPDATE info SET value = '{bank_name}' WHERE name = 'CART_BANK' ;"
                    cursor.execute(sql_bank_name)
                    connection.commit()

                    logging.info(" Transaction committed successfully")
    except Error as e:
        connection.rollback()
        logging.error(f" Error occurred, rolling back - db_convert_score:  {e} ")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

##############################################################333
def db_set_basic_info():
    find_any=db_info_exist(name='CART_NUMBER')
    if not find_any:
        db_info_insert(name='CART_NUMBER',value='6037997493542279')
        db_info_insert(name='CART_NAME',value="سامان یعقوبی")
        db_info_insert(name='CART_BANK',value="بانک ملی")

        db_info_insert(name='banner_need_approve',value="0")
        
        db_info_insert(name="bot_is_enable",value="1")
        db_info_insert(name="main_admin",value="340500740")#@saaman
    return True

