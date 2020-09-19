import datetime

from datetime import time


class Problem:

    # By default it's -1. It'll change in main.py
    AVG_SP_TIME = -1

    def __init__(self, problem_num, sp, date, longtitude=4):
        self.problem_num = problem_num
        self.sp = sp
        self.date = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M')
        self.entries_longtitude = self.sp * longtitude
        self.total_spent_hours = 0.
        # list of default tasks used to describe the problem(with dates)
        self.task_list = list()


    # When True - stop ading new tasks
    def add_task(self, task):
        self.task_list.append(task)
        return self.__add_total_spent_hours(task.get_random_time())


    def __add_total_spent_hours(self, hours):
        self.total_spent_hours += hours
        return self.is_more_than_sp_hours(self.AVG_SP_TIME)


    def is_more_than_sp_hours(self, avg_sp_time):
        return self.total_spent_hours > avg_sp_time * self.sp

    def get_problem_year(self):
        return self.date.year


    def get_problem_month(self):
        return self.date.month


    def get_problem_day(self):
        return self.date.day


    def get_date(self):
        return self.date


    def get_sp(self):
        return self.sp


    def get_task_list(self):
        return self.task_list


    def get_problem_num(self):
        return self.problem_num


    def __str__(self):
        str_represent = "PROBLEM " + str(self.problem_num) + "(sp=" + str(self.sp) + ")\n"
        str_represent += "Date"
        str_represent += "\n"
        str_represent += str(self.date)
        str_represent += "\n"
        str_represent += "\tTAKSKS:\n"
        for task in self.task_list:
            str_represent += "\t-----"
            str_represent += task.__str__()
            str_represent += "-----\n"
        str_represent += "\n"
        str_represent += "Hours spent on problem: "
        str_represent += str(self.total_spent_hours)
        str_represent += "\n"
        str_represent += "AVG SP: "
        str_represent += str(self.AVG_SP_TIME)
        
        return str_represent


    @staticmethod
    def get_total_sps(problems_list):
        total_sps = 0
        for problem in problems_list:
            total_sps += problem.get_sp()
            print(problem.get_problem_num(), problem.get_sp())

        return total_sps


    @staticmethod
    def get_working_days_num_in_range(start_date, end_date):
        working_days_num = 0
        # Key - working day: Monday, Tuesday, ...
        # Values - all dates in that day
        working_days_dict = dict()
        
        elapsed_time = end_date - start_date
        days_delta = elapsed_time.days
        for day_num in range(days_delta):
            day_dt = start_date + datetime.timedelta(days=day_num)
            if(Problem.is_workaday(day_dt.year, day_dt.month, day_dt.day)):
                working_days_num += 1
        return working_days_num


    @staticmethod
    def is_workaday(year, month, day):
        date = datetime.date(year, month, day)
        week_number = date.weekday()
        return week_number < 5


    @staticmethod
    def get_working_days(start_date, end_date):
        working_days_num = 0
        # Key - working day: Monday, Tuesday, ...
        # Values - all dates in that day
        working_days_dict = dict()
        for concrete_day in range(start_date, end_date):
            if(self.__is_workaday(concrete_day.year, concrete_day.month, concrete_day.day)):
                working_days_num += 1
                # what day in week this day is: Monday - 0, Tuesday - 1, and so on..
                day_num_in_weeek = self.__get_day_num(concrete_day.year, concrete_day.month, concrete_day.day)
                if(day_num_in_weeek not in working_days_dict.keys()):
                    working_days_dict[day_num_in_weeek] = []
                working_days_dict[day_num_in_weeek].append(datetime.date(self.year_num, self.month_num, day_num))
        return working_days_num, working_days_dict

    # за допомогою лямбди - всі понеділки пятниці і тд витащити за нехуй в одну дію. Так і зробити.