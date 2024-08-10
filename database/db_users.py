import mysql.connector # type: ignore
from configs.auth import DB_CONFIG
from configs.config import *
########################################################################
def create_user(userid,username):
     try:
        with mysql.connector.connect(**DB_CONFIG) as connection:
            with connection.cursor()  as cursor:
                sql= f"INSERT INTO users(userid,username) VALUES ({userid},'{username}')"
                cursor.execute(sql)
                connection.commit()
                return True
     except:    
          return False
     
##################################################
def get_user_info(user_id):
     sql=f"""SELECT * FROM users 
     WHERE userid= {user_id};"""
     with mysql.connector.connect(**DB_CONFIG) as connection:
          with connection.cursor()  as cursor:
               cursor.execute(sql)
               result =cursor.fetchone()
     return result
##################################################
def get_all_users():
     sql=f"SELECT * FROM users;"
     with mysql.connector.connect(**DB_CONFIG) as connection:
          with connection.cursor()  as cursor:
            cursor.execute(sql)
            result =cursor.fetchall()
            return result
##################################################

def get_user_balance(user_id):
    sql= f"SELECT balance from users where userid = {user_id}"
    with mysql.connector.connect(**DB_CONFIG) as connection:
          with connection.cursor()  as cursor:
               cursor.execute(sql)
               result =cursor.fetchone()
    return result
     
########################################################################
def get_user_score(user_id):
    sql= f"SELECT score from users where userid = {user_id}"
    with mysql.connector.connect(**DB_CONFIG) as connection:
          with connection.cursor()  as cursor:
               cursor.execute(sql)
               result =cursor.fetchone()
    return result
########################################################################
def get_user_id(user_id):
    sql= f"SELECT userid from users where userid = {user_id}"
    with mysql.connector.connect(**DB_CONFIG) as connection:
          with connection.cursor()  as cursor:
               cursor.execute(sql)
               result =cursor.fetchone()
    return result
     
########################################################################
def increase_balance(user_id,increase_amount):
    sql= f"UPDATE users SET balance = balance + {increase_amount} WHERE userid = {user_id};"
    with mysql.connector.connect(**DB_CONFIG) as connection:
          with connection.cursor()  as cursor:
               cursor.execute(sql)
               connection.commit()
########################################################################
def decrease_balance(user_id,decrease_balance_amount):
    user_balance=get_user_balance(user_id=user_id)
    if user_balance<decrease_balance_amount :
        return False
    sql= f"UPDATE users SET balance = balance - {decrease_balance_amount} WHERE userid = {user_id};"
    with mysql.connector.connect(**DB_CONFIG) as connection:
          with connection.cursor()  as cursor:
               cursor.execute(sql)
               connection.commit()

    return True
########################################################################
def increase_score(user_id,increase_amount):
    sql= f"UPDATE users SET score = score + {increase_amount} WHERE userid = {user_id};"
    with mysql.connector.connect(**DB_CONFIG) as connection:
          with connection.cursor()  as cursor:
               cursor.execute(sql)
               result =cursor.fetchone()
               connection.commit()
    return result
########################################################################
def decrease_score(user_id,decrease_amount):
    user_score=get_user_score(user_id=user_id)
    if user_score<decrease_amount :
        return False
    sql= f"UPDATE users SET score = score + {decrease_amount} WHERE userid = {user_id};"
    with mysql.connector.connect(**DB_CONFIG) as connection:
          with connection.cursor()  as cursor:
               cursor.execute(sql)
               connection.commit()

    return True
##########################################################################
def delete_user(user_id):
    sql= f"delete from users where userid ={user_id};"
    with mysql.connector.connect(**DB_CONFIG) as connection:
          with connection.cursor()  as cursor:
               cursor.execute(sql)
               connection.commit()
     
