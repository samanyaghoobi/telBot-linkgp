import logging
import mysql.connector # type: ignore
from mysql.connector import Error
from configs.auth import DB_CONFIG
from configs.config import *

#########################################################
#! reserve table 
#########################################################
#*add :save : create
def make_a_reservation(userid,price,date,time,time_index,banner,link):
    sql=f"""INSERT INTO reserve (approved, userid, price, date, time, time_index, banner, link)
VALUES (0, {userid}, {price}, '{date}', '{time}', {time_index}, '{banner}', '{link}');"""
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
        logging.error(f"error make_a_reservation:  {e} ")
########################################
#*approve
def approve_a_reserve(id):
    sql=f"""UPDATE reserve
SET approved = 1
WHERE id = {id};
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
        logging.error(f"error approve_a_reserve: {e}")    

###########################
#*get banner_with id
def get_banner_with_id_reserve(reserve_id):
     sql=f"""SELECT banner
FROM reserve
WHERE id = {reserve_id};
"""
     try:
        with mysql.connector.connect(**DB_CONFIG) as connection:
            if connection.is_connected():
                with connection.cursor()  as cursor:
                     cursor.execute(sql)
                    #  connection.commit()
                     banner=cursor.fetchone()
                     cursor.close()
                     connection.close()
                     return banner
     except Error as e:
        logging.error(f"error get_banner_with_id_reserve: {e} ")
##########################
#* get id with time and date
def get_id_with_time_date_reserve(time,date):
     sql=f"""SELECT id 
FROM reserve 
WHERE date = '{date}' AND time = '{time}';"""
     logging.error(sql)
     try:
        with mysql.connector.connect(**DB_CONFIG) as connection:
            if connection.is_connected():
                with connection.cursor()  as cursor:
                     cursor.execute(sql)
                    #  connection.commit()
                     id=cursor.fetchone()
                     cursor.close()
                     connection.close()
                     return id
     except Error as e:
         logging.error(f" error get_id_with_time_date_reserve:   {e}  ")
###############################
#* get link with id 
def get_link_with_id_reserve(id):
     sql=f"""SELECT link
FROM reserve
WHERE id = {id};
"""
     try:
        with mysql.connector.connect(**DB_CONFIG) as connection:
            if connection.is_connected():
                with connection.cursor()  as cursor:
                     cursor.execute(sql)
                    #  connection.commit()
                     link=cursor.fetchone()
                     cursor.close()
                     connection.close()
                     return link
     except Error as e:
        logging.error(f" error:   {e}  ")
#########################################
#* get links of day with date 
def get_link_with_date_reserve(date):
     sql=f"""SELECT link 
FROM reserve 
WHERE date = '{date}';
"""
     try:
        with mysql.connector.connect(**DB_CONFIG) as connection:
            if connection.is_connected():
                with connection.cursor()  as cursor:
                     cursor.execute(sql)
                     link=cursor.fetchall()
                    #  connection.commit()
                     cursor.close()
                     connection.close()
                     return link
     except Error as e:
        logging.error(f" error get_link_with_id_reserve:   {e}  ")
####################################3
#* get  all 
def get_all_reserves():
     sql=f"SELECT * FROM reserve;"
     try:
        with mysql.connector.connect(**DB_CONFIG) as connection:
            if connection.is_connected():
                with connection.cursor()  as cursor:
                     cursor.execute(sql)
                    #  connection.commit()
                     reserves=cursor.fetchall()
                     cursor.close()
                     connection.close()
                     return reserves
     except Error as e:
        logging.error(f" error get_all_reserves:   {e}  ")
#########################################################
#