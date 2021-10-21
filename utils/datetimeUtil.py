from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta

def getDate(date_str, dateFormat='%Y-%m-%d'):
    date_time_obj = datetime.strptime(date_str, dateFormat)
    return date_time_obj.date()

def getDateRange(no_of_last_month):
    today = date.today()
    last_months = date.today() + relativedelta(months=-no_of_last_month)
    return (today,last_months)

