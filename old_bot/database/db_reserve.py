import logging
import mysql.connector # type: ignore
from mysql.connector import Error
from configs.auth import DB_CONFIG
from configs.basic_info import *

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
########################################
#*change banner
def change_banner_reserve(reserve_id: int,banner :str):
    sql=f"""UPDATE reserve
SET banner = '{banner}'
WHERE id = {reserve_id};
"""
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
        logging.error(f"error change_banner_reserve: {e}")    
        return False

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
         return None
##########################
#* get id with user_id and date
def get_id_with_user_id_date_reserve(user_id :int,date):
     sql=f"""SELECT id
FROM reserve 
WHERE date = '{date}' AND userid ={user_id} ;"""
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
         return None
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
###############################
#* get approved with id 
def is_reserve_approved(id):
     sql=f"""SELECT approved
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
###############################
#* get ifno with id 
def get_info_with_reserve_id(reserve_id):
     """userid,price,date,time,time_index"""
     sql=f"""SELECT userid,price,date,time,time_index
FROM reserve
WHERE id = {reserve_id};
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
def db_reserve_get_links_within_week_reserve(interval:int=0,period:int=7):
    sql = f"""
    SELECT link 
    FROM reserve 
    WHERE date BETWEEN CURDATE()+ INTERVAL {interval} DAY AND CURDATE() + INTERVAL {period} DAY
    """
    try:
        with mysql.connector.connect(**DB_CONFIG) as connection:
            if connection.is_connected():
                with connection.cursor() as cursor:
                    cursor.execute(sql)
                    links = cursor.fetchall()
                    return links
    except Error as e:
        logging.error(f"Error in get_links_within_week_reserve: {e}")

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
####################################
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