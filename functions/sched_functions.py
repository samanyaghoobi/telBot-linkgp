from datetime import datetime
import threading
import time
import schedule
from configs.basic_info import dayClockArray
################################
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)
################################
def schedule_jobs():
    schedule.clear()
    from main import send_scheduled_message 
    for i in range(len(dayClockArray)):
        schedule.every().day.at(dayClockArray[i]).do(send_scheduled_message)

################################
def start_scheduler():
    schedule_jobs()
    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.daemon = True  # این کار باعث می‌شود Thread با بستن برنامه اصلی بسته شود
    scheduler_thread.start()
################################################
