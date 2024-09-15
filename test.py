import logging
import mysql.connector # type: ignore
from mysql.connector import Error
from configs.auth import DB_CONFIG
from configs.basic_info import dayClockArray
from database.db_creation import db_create_table_bot_info, dbCreateDatabases
from database.db_functions import db_set_basic_info
from database.db_timing import create_channel_timing, db_timing_get_free_time_for_period, get_is_free_time_for_days
from functions.calender_functions import cal_date
from database.db_info import *
from functions.custom_functions import format_cart_number_with_space
# 