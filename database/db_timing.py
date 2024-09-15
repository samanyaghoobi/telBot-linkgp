import logging
import mysql.connector # type: ignore
from mysql.connector import Error
from configs.auth import DB_CONFIG
from configs.basic_info import *
###############################################################333
def create_channel_timing(date):
    sql= f"INSERT INTO channel_timing(record_date) VALUES ('{date}');"
    timing=time_exist(date=date)
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
def time_exist(date):
    sql=f"""select record_date from channel_timing
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
                     if timing != None:
                         return True
                     return False
    except Error as e:
        logging.error(f" error get_channel_timing:   {e} ")
#################################################################
def get_id_reserver_channel_timing(date,time):
    """return id of who reserved the time , none for not reserved time"""
    from functions.custom_functions import find_index
    time_index=find_index(time,dayClockArray)
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
#################################################################
def get_is_free_time_for_days(days:int,time):
    from functions.custom_functions import find_index
    time_index=find_index(time,dayClockArray)
    db_column_time_name=db_hour_name[time_index]
    sql=f"""SELECT record_date, hour_{db_column_time_name}
FROM channel_timing
WHERE record_date BETWEEN CURRENT_DATE AND CURRENT_DATE + INTERVAL {days} DAY
AND hour_{db_column_time_name} != 0;
"""
    try:
         with mysql.connector.connect(**DB_CONFIG) as connection:
            if connection.is_connected():
                with connection.cursor()  as cursor:
                     cursor.execute(sql)
                     timing=  cursor.fetchall()
                     cursor.close()
                     connection.close()
                     return timing
    except Error as e:
        logging.error(f" error get_channel_timing:   {e} ")
####################################################################
def db_timing_get_free_time_for_period(interval:int=0,period:int=7):
    """return a array [date, times[1:22] of day] 
    0 mean full and 1 mean free time for a week"""
    sql=f"""SELECT 
    record_date,
    hour_13 = 0 AS hour_13_empty,
    hour_14 = 0 AS hour_14_empty,
    hour_15 = 0 AS hour_15_empty,
    hour_16 = 0 AS hour_16_empty,
    hour_17 = 0 AS hour_17_empty,
    hour_18 = 0 AS hour_18_empty,
    hour_18_30 = 0 AS hour_18_30_empty,
    hour_19 = 0 AS hour_19_empty,
    hour_19_30 = 0 AS hour_19_30_empty,
    hour_20 = 0 AS hour_20_empty,
    hour_20_30 = 0 AS hour_20_30_empty,
    hour_21 = 0 AS hour_21_empty,
    hour_21_30 = 0 AS hour_21_30_empty,
    hour_22 = 0 AS hour_22_empty,
    hour_22_30 = 0 AS hour_22_30_empty,
    hour_23 = 0 AS hour_23_empty,
    hour_23_30 = 0 AS hour_23_30_empty,
    hour_24 = 0 AS hour_24_empty,
    hour_24_30 = 0 AS hour_24_30_empty,
    hour_01 = 0 AS hour_01_empty,
    hour_01_30 = 0 AS hour_01_30_empty,
    hour_02 = 0 AS hour_02_empty
FROM channel_timing
WHERE record_date BETWEEN CURDATE()+ INTERVAL {interval} DAY AND CURDATE() + INTERVAL {period} DAY
AND (
    hour_13 = 0 OR
    hour_14 = 0 OR
    hour_15 = 0 OR
    hour_16 = 0 OR
    hour_17 = 0 OR
    hour_18 = 0 OR
    hour_18_30 = 0 OR
    hour_19 = 0 OR
    hour_19_30 = 0 OR
    hour_20 = 0 OR
    hour_20_30 = 0 OR
    hour_21 = 0 OR
    hour_21_30 = 0 OR
    hour_22 = 0 OR
    hour_22_30 = 0 OR
    hour_23 = 0 OR
    hour_23_30 = 0 OR
    hour_24 = 0 OR
    hour_24_30 = 0 OR
    hour_01 = 0 OR
    hour_01_30 = 0 OR
    hour_02 = 0
)
"""
    result=[1,1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    try:
            with mysql.connector.connect(**DB_CONFIG) as connection:
                if connection.is_connected():
                    with connection.cursor()  as cursor:
                            cursor.execute(sql)
                            days=  cursor.fetchall()
                            cursor.close()
                            connection.close()
                            for day in days:
                                for index in range(len(day)):
                                    if day[index] !=1:
                                            result[index]=0
                            result[0]=9
                            return result
    except Error as e:  
        logging.error(f" error db_timing_get_week_free_time:   {e} ")