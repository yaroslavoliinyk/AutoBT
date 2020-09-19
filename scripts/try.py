from datetime import datetime
from datetime import date
from datetime import timedelta

start_dt = "2010-09-04"
end_dt   = "2020-09-10"

START_DT = date.fromisoformat(start_dt)
print(START_DT.weekday())
END_DT = date.fromisoformat(end_dt)

print(START_DT, END_DT)
elapsed_time = END_DT - START_DT
print(elapsed_time)

days_delta = elapsed_time.days


l = [1, 2, 3, 4, 5]
print(l.pop(0))
print(l.pop(0))
print(l)
#for day_dt in range(days_delta):
    #print(START_DT+timedelta(days=day_dt))
