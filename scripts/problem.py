import datetime


from datetime import time
from bugtracker_entry import BugTrackerEntry


class Problem:

    def __init__(self, problem_num, date, sp, longtitude=4):
        self.problem_num = problem_num
        self.date = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M.%f')
        self.sp = sp
        self.entries_longtitude = self.sp * longtitude
        self.total_spent_hours = 0.
        # sequence number(kind of id like #1, #2, #3) of entry written to bugtracker
        self.entry_number = 0
        # list of default tasks used to describe the problem(with dates)
        self.task_list = dict()


    # When True - stop ading new tasks
    def add_task_and_time(self, task):
        if(self.entry_number < 2):
            task_date = self.date
        elif(self.entry_number < 4):
            task_date = self.date + datetime.timedelta(days=1)
        else:
            task_date = self.date + datetime.timedelta(days=self.entry_number-2)
        #! Here's pretty silly solution if the task goes on to the next month
        # TODO: Solve in more beautiful way(for now we will write everything to the first day of the task)
        if(task_date.month != self.date.month):
            task_date = self.date.month

        if self.task_list[task_date] is None:
            self.task_list[task_date] = []
        self.task_list[task_date].append(task)
        
        # The algorithm is as follows: 
        # entry 0 - day 1; entry 1 - day 1; entry 2 - day 2; entry 3 - day 2;
        # entry 4 - day 3; entry 5 - day 4; entry 6 - day 5 and so on
        self.entry_number += 1
        return self.__add_total_spent_hours(task.get_random_time())


    def __add_total_spent_hours(self, hours):
        self.total_spent_hours += hours
        return self.__is_more_than_sp_hours(BugTrackerEntry.AVG_SP_TIME)


    def __is_more_than_sp_hours(self, avg_sp_time):
        return self.total_spent_hours > avg_sp_time * self.sp

    def get_problem_year(self):
        return self.date.year


    def get_problem_month(self):
        return self.date.month


    def get_problem_day(self):
        return self.date.day


    def get_sp(self):
        return self.sp


    @staticmethod
    def get_problems_by_month(tasks_list, month_number):
        month_problems = []
        for problem in problems_list:
            if(month_number == problem.get_problems_month()):
                month_problems.append(problem)
        
        return month_problems

    @staticmethod
    def get_total_sps(problems_list):
        total_sps = 0
        for problem in problems_list:
            total_sps += problem.get_sp()

        return total_sps