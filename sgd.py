\
# sql="""SELECT 
#     record_date,
#     hour_13 = 0 AS hour_13_empty,
#     hour_14 = 0 AS hour_14_empty,
#     hour_15 = 0 AS hour_15_empty,
#     hour_16 = 0 AS hour_16_empty,
#     hour_17 = 0 AS hour_17_empty,
#     hour_18 = 0 AS hour_18_empty,
#     hour_18_30 = 0 AS hour_18_30_empty,
#     hour_19 = 0 AS hour_19_empty,
#     hour_19_30 = 0 AS hour_19_30_empty,
#     hour_20 = 0 AS hour_20_empty,
#     hour_20_30 = 0 AS hour_20_30_empty,
#     hour_21 = 0 AS hour_21_empty,
#     hour_21_30 = 0 AS hour_21_30_empty,
#     hour_22 = 0 AS hour_22_empty,
#     hour_22_30 = 0 AS hour_22_30_empty,
#     hour_23 = 0 AS hour_23_empty,
#     hour_23_30 = 0 AS hour_23_30_empty,
#     hour_24 = 0 AS hour_24_empty,
#     hour_24_30 = 0 AS hour_24_30_empty,
#     hour_01 = 0 AS hour_01_empty,
#     hour_01_30 = 0 AS hour_01_30_empty,
#     hour_02 = 0 AS hour_02_empty
# FROM channel_timing
# WHERE record_date BETWEEN CURDATE() AND CURDATE() + INTERVAL 7 DAY
# AND (
#     hour_13 = 0 OR
#     hour_14 = 0 OR
#     hour_15 = 0 OR
#     hour_16 = 0 OR
#     hour_17 = 0 OR
#     hour_18 = 0 OR
#     hour_18_30 = 0 OR
#     hour_19 = 0 OR
#     hour_19_30 = 0 OR
#     hour_20 = 0 OR
#     hour_20_30 = 0 OR
#     hour_21 = 0 OR
#     hour_21_30 = 0 OR
#     hour_22 = 0 OR
#     hour_22_30 = 0 OR
#     hour_23 = 0 OR
#     hour_23_30 = 0 OR
#     hour_24 = 0 OR
#     hour_24_30 = 0 OR
#     hour_01 = 0 OR
#     hour_01_30 = 0 OR
#     hour_02 = 0
# )
# """
# result=[1,1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
# try:
#         with mysql.connector.connect(**DB_CONFIG) as connection:
#             if connection.is_connected():
#                 with connection.cursor()  as cursor:
#                         cursor.execute(sql)
#                         days=  cursor.fetchall()
#                         cursor.close()
#                         connection.close()
#                         for day in days:
#                             for index in range(len(day)):
#                                 if day[index] !=1:
#                                         print(index)
#                                         result[index]=0
#                         print(result)
# except Error as e:
#     logging.error(f" error get_channel_timing:   {e} ")