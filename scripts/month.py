import datetime
import calendar
import logics

class Month:

    # Number of hours in one month of work
    HOURS = 130.
    AVG_HOUR_PER_DAY = 6.5
    WORK_COEF = 0.75
    SUPPORT_COEF = 1.-WORK_COEF



    def __init__(self, current_month, month_flag=True):
        # Describes if it's a current month or previous
        # True if current, False if previous
        self.current_month = current_month
        # True if we write tasks to this month, false if not
        self.month_flag = month_flag

    
    def __init__(self, link, current_month, month_flag=True):
        self.link = link
        self.current_month = current_month
        self.month_flag = month_flag
        # When the last time I tracked time to work
        # None - empty week; date - last work time
        self.last_commit = None
        self.start_day_num = None
        if(self.current_month == True):
            self.year_num = datetime.datetime.today().year
            self.month_num = datetime.datetime.today().month
            self.last_day_num = datetime.datetime.today().day
        else:
            self.month_num = datetime.datetime.today().month-1
            # if previous month is less than January then we need to subtract a year and set month_num = 12
            if(self.month_num == 0):
                self.year_num = datetime.datetime.today().year-1
                self.month_num = 12
            self.last_day_num = calendar.monthrange(self.year_num, self.month_num)[1]
            

    def set_link(self, link):
        self.link = link


    # Already worked for X hours
    def set_hours(self, hours): 
        self.hours = hours


    def set_last_commit(self, last_commit):
        self.last_commit = last_commit
        # Means that there are no records about commits this month
        if(last_commit is None):
            self.start_day_num = 1
        else:
            self.start_day_num = last_commit.day+1
        # Calculate how much hours I need to work a day
        self.__calculate_work_time_a_day()

    def get_link(self):
        return self.link


    def get_hours(self):
        return self.hours


    def get_flag(self):
        return self.month_flag


    def get_last_commit(self):
        return self.last_commit


    def get_work_time_a_day(self):
        return self.work_time_a_day


    def get_working_days_number(self):
        working_days_num = 0
        for day_num in range(self.start_day_num, self.last_day_num):
            if(self.__is_workaday(self.year_num, self.month_num, day_num)):
                working_days_num += 1
        return working_days_num



    def __is_workaday(self, year, month, day):
        date = datetime.date(year, month, day)
        week_number = date.weekday()
        return week_number < 5


    def __calculate_work_time_a_day(self):
        # If we start to fill from day 1, then it will be a default working time a day
        if(self.start_day_num == 1):
            # If we consider taking this concrete month
            # Then work time a day will be 130hrs/20 = 6.5 hours a day
            # It will be different for previous month since it's not precise 
            # 20 - is approximate number of working days a month
            self.work_time_a_day = HOURS / 20
        else:
            working_days_num_remain = len(logics.get_working_days(self.start_day_num, self.last_day_num, self.month_num, self.year_num))
            working_days_hours_remain = HOURS - self.hours
            self.work_time_a_day = working_days_hours_remain / working_days_num_remain

        
        