import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG

def db_execution(sql:str):
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

