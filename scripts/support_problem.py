from task import Task
from random import randrange
from problem import Problem

import time


class SupportProblem:

    PROBLEM_ID   = "7571"
    date_list    = list()
    

    def __init__(self, date_list, support_time):
        self.date_list = date_list
        self.support_time = support_time
        
        # The list, all the tasks will be in
        self.support_task_list = []


    def add_task_and_time(self, new_random_support_task, random_date):
            # Adding new task
            new_support_task = Task(new_random_support_task.get_name(), new_random_support_task.get_from_time(), new_random_support_task.get_to_time(),
                                                    new_random_support_task.get_freq_coef(), new_random_support_task.get_is_work_task())
            
            new_support_task.set_date(random_date)
            self.support_task_list.append(new_support_task)
            # Subtracting time
            self.support_time -= new_support_task.get_random_time()


    def fulfill_with_special_tasks(self, daily, tech_improvement, review_plan_retro):
        # Monday, Tuesday, Wednesday, Thursday
        daily_days = list(filter(lambda date_day: date_day.weekday()<5, self.date_list))
        for daily_day in daily_days:
            new_daily_task = Task(daily.get_name(), daily.get_from_time(), daily.get_to_time(), daily.get_freq_coef(), daily.get_is_work_task())
            new_daily_task.set_date(daily_day)
            new_daily_task.set_random_time(daily.get_from_time())
            self.support_task_list.append(new_daily_task)
        
        # Wednesday
        tech_improvement_days = list(filter(lambda date_day: date_day.weekday()==3, self.date_list))
        for ti_day in tech_improvement_days:
            new_tech_improv_task = Task(tech_improvement.get_name(), tech_improvement.get_from_time(), 
                                        tech_improvement.get_to_time(), tech_improvement.get_freq_coef(), tech_improvement.get_is_work_task())
            new_tech_improv_task.set_date(ti_day)
            self.support_task_list.append(new_tech_improv_task)

        #Friday
        # Append all retro review plan
        review_plan_retro_days = list(filter(lambda date_day: date_day.weekday()==5, self.date_list))
        # Because we have retro plan review once 2 weeks(not once a week as earlier)
        #_ = review_plan_retro_days.pop(0)
        for rpr_day in review_plan_retro_days:
            new_retro_task = Task(review_plan_retro.get_name(), review_plan_retro.get_from_time(), 
                                        review_plan_retro.get_to_time(), review_plan_retro.get_freq_coef(), review_plan_retro.get_is_work_task())
            new_retro_task.set_date(rpr_day)
            self.support_task_list.append(new_retro_task)
      
               
        # In the very end we need to calculate how much time we have left to other tasks to manipulate
        # Here we've set in months vaalues how much time was left for other tasks except obligatory
        used_time = 0.
        for task in self.support_task_list:
            used_time += task.get_random_time()
        
        # Subtracting support time
        self.support_time -= used_time
        

    def get_support_time(self):
        return self.support_time

    
    def get_support_task_list(self):
        return self.support_task_list

