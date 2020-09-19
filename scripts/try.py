from datetime import datetime
from datetime import date
from datetime import timedelta

start_dt = "2010-09-01"
end_dt   = "2020-09-10"

START_DT = date.fromisoformat(start_dt)
END_DT = date.fromisoformat(end_dt)

print(START_DT, END_DT)
elapsed_time = END_DT - START_DT
print(elapsed_time)

days_delta = elapsed_time.days


#for day_dt in range(days_delta):
    #print(START_DT+timedelta(days=day_dt))
