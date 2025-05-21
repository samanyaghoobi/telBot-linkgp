

import jdatetime

def dateInPersian(date_obj):
    return jdatetime.date.fromgregorian(date=date_obj)

def date_to_persian(date_obj):
    jdate = jdatetime.date.fromgregorian(date=date_obj)
    return jdate.strftime("%Y-%m-%d")