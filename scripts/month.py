



class Month:

    # Number of hours in one month to work
    HOURS = 130.

    def __init__(self, month_flag=True):
        this.month_flag = month_flag
        pass

    
    def __init__(self, link, month_flag=True):
        self.link = link
        self.month_flag = month_flag


    def set_link(self, link):
        self.link = link


    def set_hours(self, hours):
        self.hours = hours


    def get_link(self):
        return self.link


    def get_hours(self):
        return self.hours


    def get_flag(self):
        return self.month_flag