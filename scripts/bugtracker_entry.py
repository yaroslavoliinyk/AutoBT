from problem import Problem
from month import Month


class BugTrackerEntry:

    AVG_SP_TIME = BugTrackerEntry.calculate_avg_sp_time(months_list, problems_list)

    def __init__(self, problem, task, random_task_time):
        self.problem = problem
        self.task = task
        self.random_task_time = random_task_time


    @staticmethod
    def calculate_avg_sp_time(months_list, problems_list):
        working_days_number = 0
        for month in months_list:
            working_days_number += month.get_working_days_number()

        sp_number = Problem.get_total_sps(problems_list)
        # Formula to calculate how many hours was delegated to developing throught the given perioud
        working_days_hours = working_days_number * Month.AVG_HOUR_PER_DAY * Month.WORK_COEF
        avg_sp_time = working_days_hours / sp_number
        return avg_sp_time