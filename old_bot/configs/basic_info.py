
#vars
max_len_name=20
max_len_member=8
max_len_des=30
##############################################################
days_of_week_name = ["دوشنبه", "سه‌شنبه", "چهارشنبه", "پنج‌شنبه", "جمعه", "شنبه", "یک‌شنبه"]
months = ["January",   "February",  "March",     "April",     "May",       "June",      "July",      "August",    "September", "October",   "November",  "December"   ]
dayClockArray=["13:00","14:00","15:00","16:00","17:00","18:00","18:30","19:00","19:30","20:00","20:30","21:00","21:30","22:00","22:30","23:00","23:30","00:00","00:30","01:00","01:30","02:00"]
db_hour_name=["13","14","15","16","17","18","18_30","19","19_30","20","20_30","21","21_30","22","22_30","23","23_30","24","24_30","01","01_30","02"]
##############################################################
base_score=10 # all time must be 10
base_score_value=8
price_1=8
price_2=15
price_3=25
price_plans=[price_1,price_2,price_3]
price_plan1_off=90  # plus 15% = 103
price_plan2_off=180 # plus 20% = 216
price_plan3_off=337 # plus 25% = 421
price_plan1=103  # plus 15% = 103
price_plan2=216 # plus 20% = 216
price_plan3=421 # plus 25% = 421
plans=[price_1,price_2,price_3,price_plan1_off,price_plan2_off,price_plan3_off]
plans_off=[price_plan1_off,price_plan2_off,price_plan3_off]
plans_off_real=[price_plan1,price_plan2,price_plan3]
##############################################################
creator_username="@saaman"
time_duration_def="00:30"
##############################################################
default_banner_pattern=r"""^Super\ GP\n
        \n
        naмe\ :\ .+\n
        \n
        мeмвer:\ .+\n
        \n
        lιnĸ:\ .+\n
        \n
        @LinkGP$"""
