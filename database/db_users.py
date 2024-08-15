import logging
import mysql.connector # type: ignore
from mysql.connector import Error
from configs.auth import DB_CONFIG
from configs.config import *
########################################################################
def create_user(userid,username):
    user_exists=get_user_info(user_id=userid)
    if not user_exists:
        sql= f"INSERT INTO users(userid,username) VALUES ({userid},'{username}')"
        try:
            with mysql.connector.connect(**DB_CONFIG) as connection:
                if connection.is_connected():
                    with connection.cursor()  as cursor:
                        cursor.execute(sql)
                        connection.commit()
                        cursor.close()
                        connection.close()
        except Error as e:
            logging.error(f"\033[91merror create_user: \n {e} \n \033[0m")
    else:
        logging.error("user_exists")
##################################################
def get_user_info(user_id):
    sql=f"""SELECT * FROM users 
WHERE userid= {user_id};"""
    try:
        with mysql.connector.connect(**DB_CONFIG) as connection:
            if connection.is_connected():
                with connection.cursor()  as cursor:
                     cursor.execute(sql)
                    #  connection.commit()
                     user = cursor.fetchone()
                     cursor.close()
                     connection.close()
                     return user
    except Error as e:
        logging.error(f"\033[91merror get_user_info: \n {e} \n \033[0m")
############################
def get_all_users():
    sql=f"SELECT * FROM users;"
    try:
        with mysql.connector.connect(**DB_CONFIG) as connection:
            if connection.is_connected():
                with connection.cursor()  as cursor:
                     cursor.execute(sql)
                    #  connection.commit()
                     users=cursor.fetchall()
                     cursor.close()
                     connection.close()
                     return users
    except Error as e:
        logging.error(f"\033[91merror get_all_users: \n {e} \n \033[0m")
##################################################

def get_user_balance(user_id):
    sql= f"SELECT balance from users where userid = {user_id}"
    try:
        with mysql.connector.connect(**DB_CONFIG) as connection:
            if connection.is_connected():
                with connection.cursor()  as cursor:
                     cursor.execute(sql)
                    #  connection.commit()
                     balance=cursor.fetchone()
                     cursor.close()
                     connection.close()
                     return balance[0]
    except Error as e:
        logging.error(f"\033[91merror get_user_balance: \n {e} \n \033[0m")
########################################################################
def get_user_score(user_id):
    sql= f"SELECT score from users where userid = {user_id}"
    try:
        with mysql.connector.connect(**DB_CONFIG) as connection:
            if connection.is_connected():
                with connection.cursor()  as cursor:
                     cursor.execute(sql)
                    #  connection.commit()
                     score=cursor.fetchone()
                     cursor.close()
                     connection.close()
                     return score[0]
    except Error as e:
        logging.error(f"\033[91merror get_user_score: \n {e} \n \033[0m")
########################################################################
def get_user_id(user_id):
    sql= f"SELECT userid from users where userid = {user_id}"
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
        logging.error(f"\033[91merror get_user_id: \n {e} \n \033[0m")
     
########################################################################
def get_username(user_id):
    sql= f"SELECT username from users where userid = {user_id}"
    try:
        with mysql.connector.connect(**DB_CONFIG) as connection:
            if connection.is_connected():
                with connection.cursor()  as cursor:
                     cursor.execute(sql)
                    #  connection.commit()
                     username=cursor.fetchone()
                     cursor.close()
                     connection.close()
                     return username[0]
    except Error as e:
        logging.error(f"\033[91merror get_user_id: \n {e} \n \033[0m")
     
########################################################################
def increase_balance(user_id,increase_amount):
    sql= f"UPDATE users SET balance = balance + {increase_amount} WHERE userid = {user_id};"
    try:
        with mysql.connector.connect(**DB_CONFIG) as connection:
            if connection.is_connected():
                with connection.cursor()  as cursor:
                     cursor.execute(sql)
                     connection.commit()
                     cursor.close()
                     connection.close()
    except Error as e:
        logging.error(f"\033[91merror increase_balance: \n {e} \n \033[0m")
########################################################################
def decrease_balance(user_id,decrease_balance_amount):
    user_balance=int(get_user_balance(user_id=user_id))
    if user_balance<decrease_balance_amount :
        return False
    sql= f"UPDATE users SET balance = balance - {decrease_balance_amount} WHERE userid = {user_id};"
    try:
        with mysql.connector.connect(**DB_CONFIG) as connection:
            if connection.is_connected():
                with connection.cursor()  as cursor:
                     cursor.execute(sql)
                     connection.commit()
                     cursor.close()
                     connection.close()
    except Error as e:
        logging.error(f"\033[91merror decrease_balance: \n {e} \n \033[0m")
########################################################################
def increase_score(user_id,increase_amount):
    sql= f"UPDATE users SET score = score + {increase_amount} WHERE userid = {user_id};"
    try:
        with mysql.connector.connect(**DB_CONFIG) as connection:
            if connection.is_connected():
                with connection.cursor()  as cursor:
                     cursor.execute(sql)
                     connection.commit()
                     cursor.close()
                     connection.close()
    except Error as e:
        logging.error(f"\033[91merror increase_score: \n {e} \n \033[0m")
########################################################################
def decrease_score(user_id,decrease_amount ):
    user_score=get_user_score(user_id=user_id)
    if user_score<decrease_amount :
        return False
    sql= f"UPDATE users SET score = score + {decrease_amount} WHERE userid = {user_id};"
    try:
        with mysql.connector.connect(**DB_CONFIG) as connection:
            if connection.is_connected():
                with connection.cursor()  as cursor:
                     cursor.execute(sql)
                     connection.commit()
                     cursor.close()
                     connection.close()
    except Error as e:
        logging.error(f"\033[91merror decrease_score: \n {e} \n \033[0m")
        
##########################################################################
def delete_user(user_id):
    sql= f"delete from users where userid ={user_id};"
    try:
        with mysql.connector.connect(**DB_CONFIG) as connection:
            if connection.is_connected():
                with connection.cursor()  as cursor:
                     cursor.execute(sql)
                     connection.commit()
                     cursor.close()
                     connection.close()
    except Error as e:
        logging.error(f"\033[91merror delete_user: \n {e} \n \033[0m")