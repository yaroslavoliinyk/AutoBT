



class Month:

    # Number of hours in one month of work
    HOURS = 130.
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


    def set_link(self, link):
        self.link = link


    def set_hours(self, hours):
        self.hours = hours


    def set_last_commit(self, last_commit):
        self.last_commit = last_commit

    def get_link(self):
        return self.link


    def get_hours(self):
        return self.hours


    def get_flag(self):
        return self.month_flag


    def get_last_commit(self):
        return self.last_commit

