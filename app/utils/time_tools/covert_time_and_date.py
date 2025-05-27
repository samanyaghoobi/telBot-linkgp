import jdatetime
from datetime import date, datetime

def dateInPersian(date_obj):
    return jdatetime.date.fromgregorian(date=date_obj)

def date_to_persian(date_obj):
    jdate = jdatetime.date.fromgregorian(date=date_obj)
    return jdate.strftime("%Y-%m-%d")

def date_to_persian_str(gregorian_date: date) -> str:
    if isinstance(gregorian_date, datetime):
        gregorian_date = gregorian_date.date()
    jdate = jdatetime.date.fromgregorian(date=gregorian_date)
    return jdate.strftime("%d-%m-%Y")