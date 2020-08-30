import datetime
from datetime import date


def is_workaday(year, month, day):
        date = datetime.date(year, month, day)
        week_number = date.weekday()
        return week_number < 5

print(is_workaday(2020, 8, 31))