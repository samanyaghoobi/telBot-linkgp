import logging
import mysql.connector # type: ignore
from mysql.connector import Error
from configs.auth import DB_CONFIG
from configs.config import *
from functions.custom_functions import find_index
###############################################################333
def create_channel_timing(date):
    sql= f"INSERT INTO channel_timing(record_date) VALUES ('{date}');"
    timing=get_channel_timing(date=date)
    if not timing:
      try:
          with mysql.connector.connect(**DB_CONFIG) as connection:
              if connection.is_connected():
                  with connection.cursor()  as cursor:
                      cursor.execute(sql)
                      connection.commit()
                      cursor.close()
                      connection.close()
      except Error as e:
          logging.error(f" error create_channel_timing:   {e} ")
####################################################################
def update_channel_timing(time_index,userid,date):
    time=db_hour_name[time_index]
    sql=f"""UPDATE channel_timing
SET hour_{time} = {userid}
WHERE record_date = '{date}';"""
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
        logging.error(f" error update_channel_timing:   {e} ")
        return False
#################################################################
def get_channel_timing(date):
    sql=f"""select * from channel_timing
WHERE record_date = '{date}';"""
    try:
        with mysql.connector.connect(**DB_CONFIG) as connection:
            if connection.is_connected():
                with connection.cursor()  as cursor:
                     cursor.execute(sql)
                    #  connection.commit()
                     timing=cursor.fetchone()
                     cursor.close()
                     connection.close()
                     return timing
    except Error as e:
        logging.error(f" error get_channel_timing:   {e} ")
#################################################################
def get_id_reserver_channel_timing(date,time):
    """return id of who reserved the time , none for not reserved time"""
    time_index=find_index(time,time_of_day)
    db_column_time_name=db_hour_name[time_index]
    sql=f"""select hour_{db_column_time_name} from channel_timing
WHERE record_date = '{date}' AND hour_{db_column_time_name} <> 0;"""
    try:
        with mysql.connector.connect(**DB_CONFIG) as connection:
            if connection.is_connected():
                with connection.cursor()  as cursor:
                     cursor.execute(sql)
                    #  connection.commit()
                     timing=cursor.fetchone()
                     cursor.close()
                     connection.close()
                     return timing
    except Error as e:
        logging.error(f" error get_channel_timing:   {e} ")