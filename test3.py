from datetime import datetime
from configs.auth import ADMIN_ID_LIST, CHANNELS_USERNAME
from database.db_reserve import get_banner_with_id_reserve, get_id_with_time_date_reserve
from database.db_timing import check_time_date,update_channel_timing
from functions.custom_functions import find_index, get_current_date
from configs.config import time_of_day  

# print(result)