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
        # sequence number(kind of id like #1, #2, #3) of entry written to bugtracker
        self.entry_number = 0
        # list of default tasks used to describe the problem(with dates)
        self.task_dict = dict()


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
            task_date = self.date

        if task_date not in self.task_dict.keys():
            self.task_dict[task_date] = []
        self.task_dict[task_date].append(task)
        
        task.set_date(task_date)
        
        # The algorithm is as follows: 
        # entry 0 - day 1; entry 1 - day 1; entry 2 - day 2; entry 3 - day 2;
        # entry 4 - day 3; entry 5 - day 4; entry 6 - day 5 and so on
        self.entry_number += 1
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


    def get_sp(self):
        return self.sp


    def get_task_dict(self):
        return self.task_dict


    def get_problem_num(self):
        return self.problem_num


    def __str__(self):
        str_represent = "PROBLEM " + str(self.problem_num) + "(sp=" + str(self.sp) + ")\n"
        str_represent += "Date"
        str_represent += "\n"
        str_represent += str(self.date)
        str_represent += "\n"
        str_represent += "\tTAKSKS:\n"
        for task_list in list(self.task_dict.values()):
            for task in task_list:
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