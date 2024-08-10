import mysql.connector # type: ignore
from configs.auth import DB_CONFIG
from configs.config import *

#########################################################
#! reserve table 
#########################################################
#*add :save : create
def make_a_reservation(userid,price,date,time,time_index,banner,link):
    sql=f"""INSERT INTO reserve (approved, userid, price, date, time, time_index, banner, link)
VALUES (0, {userid}, {price}, '{date}', '{time}', {time_index}, '{banner}', '{link}');
"""
    print(sql)
    try:
        with mysql.connector.connect(**DB_CONFIG) as connection:
                    with connection.cursor()  as cursor:
                       result= cursor.execute(sql)
                       print(result)
                       connection.commit()
        return True
    except:
         return False
#*approve
def approve_a_reserve(id):
    sql=f"""UPDATE reserve
SET approved = 1
WHERE id = {id};
"""
    try:
        with mysql.connector.connect(**DB_CONFIG) as connection:
                    with connection.cursor()  as cursor:
                        cursor.execute(sql)
                        connection.commit()
        return True
    except:
         return False
#*get banner_with id
def get_banner_with_id_reserve(id):
     sql=f"""SELECT banner
FROM reserve
WHERE id = {id};
"""
     with mysql.connector.connect(**DB_CONFIG) as connection:
          with connection.cursor()  as cursor:
            cursor.execute(sql)
            result =cursor.fetchone()
            return result
#* get id with time and date
def get_id_with_time_date_reserve(time,date):
     sql=f"""SELECT id 
FROM reserve 
WHERE date = '{date}' AND time = '{time}';"""
     with mysql.connector.connect(**DB_CONFIG) as connection:
          with connection.cursor()  as cursor:
            cursor.execute(sql)
            result =cursor.fetchone()
            return result

#* get link with id 
def get_link_with_id_reserve(id):
     sql=f"""SELECT link
FROM reserve
WHERE id = {id};
"""
     with mysql.connector.connect(**DB_CONFIG) as connection:
          with connection.cursor()  as cursor:
            cursor.execute(sql)
            result =cursor.fetchone()
            return result


#* get links of day with date 
def get_link_with_id_reserve(date):
     sql=f"""SELECT link 
FROM reserve 
WHERE date = '{date}';
"""
     with mysql.connector.connect(**DB_CONFIG) as connection:
          with connection.cursor()  as cursor:
            cursor.execute(sql)
            result =cursor.fetchall()
            return result

#* get  all 
def get_all_reserves():
     sql=f"SELECT * FROM reserve;"
     with mysql.connector.connect(**DB_CONFIG) as connection:
          with connection.cursor()  as cursor:
            cursor.execute(sql)
            result =cursor.fetchall()
            return result
#########################################################
#