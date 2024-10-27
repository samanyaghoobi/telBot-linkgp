import logging
import mysql.connector # type: ignore
from mysql.connector import Error

from configs.auth import DB_CONFIG

#######################################
def db_info_insert(name:str,value:str):
    sql= f"INSERT INTO info(name,value) VALUES ('{name}','{value}');"
    try:
        with mysql.connector.connect(**DB_CONFIG) as connection:
            if connection.is_connected():
                with connection.cursor()  as cursor:
                    cursor.execute(sql)
                    result=connection.commit()
                    cursor.close()
                    connection.close()
                    return result
    except Error as e:
        logging.error(f" error db_info_insert:  {e}  ")

#######################################
def db_info_getValue(name:str):
    sql= f"SELECT value FROM bot_setting WHERE name = '{name}' ;"
    try:
        with mysql.connector.connect(**DB_CONFIG) as connection:
            if connection.is_connected():
                with connection.cursor()  as cursor:
                    cursor.execute(sql)
                    value=cursor.fetchone()
                    cursor.close()
                    connection.close()
                    return value
    except Error as e:
        logging.error(f" error db_info_getValue:  {e}  ")
#######################################
def db_info_exist(name:str):
    sql= f"SELECT * FROM bot_setting WHERE name = '{name}' ;"
    try:
        with mysql.connector.connect(**DB_CONFIG) as connection:
            if connection.is_connected():
                with connection.cursor()  as cursor:
                    cursor.execute(sql)
                    value=cursor.fetchone()
                    cursor.close()
                    connection.close()
                    if value is not None:
                        return True
                    return False
    except Error as e:
        logging.error(f" error db_info_getValue:  {e}  ")
#######################################
def db_info_getAll():
    sql= f"SELECT * FROM info;"
    try:
        with mysql.connector.connect(**DB_CONFIG) as connection:
            if connection.is_connected():
                with connection.cursor()  as cursor:
                    cursor.execute(sql)
                    infos=cursor.fetchall()
                    cursor.close()
                    connection.close()
                    return infos
    except Error as e:
        logging.error(f" error db_info_getValue:  {e}  ")

#######################################
def db_info_updateValue(name:str,newValue:str):
    sql= f"UPDATE bot_setting SET value = '{newValue}' WHERE name = 'name' ;"
    try:
        with mysql.connector.connect(**DB_CONFIG) as connection:
            if connection.is_connected():
                with connection.cursor()  as cursor:
                    cursor.execute(sql)
                    connection.commit()
                    cursor.close()
                    connection.close()
    except Error as e:
        logging.error(f" error db_info_changeValue:  {e}  ")
#######################################
def db_info_delete(name:str):
    sql= f"DELETE FROM bot_setting WHERE name = '{name}';"
    try:
        with mysql.connector.connect(**DB_CONFIG) as connection:
            if connection.is_connected():
                with connection.cursor()  as cursor:
                    cursor.execute(sql)
                    connection.commit()
                    cursor.close()
                    connection.close()
    except Error as e:
        logging.error(f" error db_info_delete:  {e}  ")
#######################################