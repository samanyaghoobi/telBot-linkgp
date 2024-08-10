import mysql.connector # type: ignore
from configs.auth import DB_CONFIG
from configs.config import *

def create_channel_timing(day):
    sql= f"INSERT INTO channel_timing(record_date) VALUES ('{day}');"
    try:
            with mysql.connector.connect(**DB_CONFIG) as connection:
              with connection.cursor()  as cursor:
                cursor.execute(sql)
                connection.commit()
            return True
    except:
           return False
####################################################################
def update_channel_timing(time_index,userid,date):
    time=db_hour_name[time_index]
    sql=f"""UPDATE channel_timing
SET hour_{time} = {userid}
WHERE record_date = '{date}';"""
    try:
            print("try")
            with mysql.connector.connect(**DB_CONFIG) as connection:
              with connection.cursor()  as cursor:
                result=cursor.execute(sql)
                result= connection.commit()
            return True
    except:
           return False
    
