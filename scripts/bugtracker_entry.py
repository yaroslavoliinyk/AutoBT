
from month import Month
from problem import Problem

class BugTrackerEntry:

   
    def __init__(self, problem, task, random_task_time):
        self.problem = problem
        self.task = task
        self.random_task_time = random_task_time

    