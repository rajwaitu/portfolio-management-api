from datetime import date
from datetime import datetime

def getDate(date_str, dateFormat='%Y-%m-%d'):
    date_time_obj = datetime.strptime(date_str, dateFormat)
    return date_time_obj.date()
