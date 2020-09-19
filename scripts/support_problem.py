from month import Month
from default_task import Default_Task
from random import randrange
from problem import Problem

import time


class SupportProblem:

    PROBLEM_ID = "7571"
    date_list  = list()

    def __init__(self, date_list):
        self.date_list = date_list
        self.time_used  = 0.
        
        # The list, all the tasks will be in
        self.support_task_list = []


    def add_task_and_time(self, new_random_support_task):
            new_support_task = Default_Task(new_random_support_task.get_name(), new_random_support_task.get_from_time(), new_random_support_task.get_to_time(),
                                                    new_random_support_task.get_freq_coef(), new_random_support_task.get_is_work_task())
            self.support_task_list.append(new_support_task)



    def fulfill_with_special_tasks(self, daily, tech_improvement, review_plan_retro):
        # Monday, Tuesday, Wednesday, Thursday
        daily_days = list(filter(lambda date_day: date_day.weekday()<5, self.date_list))
        for daily_day in daily_days:
            new_daily_task = Default_Task(daily.get_name(), daily.get_from_time(), daily.get_to_time(), daily.get_freq_coef(), daily.get_is_work_task())
            new_daily_task.set_date(daily_day)
            new_daily_task.set_random_time(daily.get_from_time())
            self.support_task_list.append(new_daily_task)
        
        # Wednesday
        tech_improvement_days = list(filter(lambda date_day: date_day.weekday()==2, self.date_list))
        for ti_day in tech_improvement_days:
            new_tech_improv_task = Default_Task(tech_improvement.get_name(), tech_improvement.get_from_time(), 
                                        tech_improvement.get_to_time(), tech_improvement.get_freq_coef(), tech_improvement.get_is_work_task())
            new_tech_improv_task.set_date(ti_day)
            self.support_task_list.append(new_tech_improv_task)

        #Friday
        # Append all retro review plan
        review_plan_retro_days = list(filter(lambda date_day: date_day.weekday()==4, self.date_list))
        for rpr_day in review_plan_retro_days:
             new_retro_task = Default_Task(review_plan_retro.get_name(), review_plan_retro.get_from_time(), 
                                        review_plan_retro.get_to_time(), review_plan_retro.get_freq_coef(), review_plan_retro.get_is_work_task())
            new_retro_task.set_date(rpr_day)
            self.support_task_list.append(new_retro_task)
      
               
        # In the very end we need to calculate how much time we have left to other tasks to manipulate
        # Here we've set in months vaalues how much time was left for other tasks except obligatory
        used_time = 0.
        for task in self.support_task_list:
            used_time += task.get_random_time()
        

    def get_support_task_list(self):
        return self.support_task_list


    def __set_remaining_time_for_support_task(self):
        used_time = 0.
        # ! Here is costil with months. Update in the upcoming versions
        self.different_months = dict()
        for task in self.support_task_list:
            used_time += task.get_random_time()
            # on months division
            task_month = task.get_date()
            if(task_month not in self.different_months.keys()):
                self.different_months[task_month] = []
            self.different_months[task_month].append(task)
            
        # ! Costil!!!!
        self.prev_month = None
        self.this_month = None
        if(len(self.months) == 2):
            self.prev_month = self.months[0]
            prev_month_tasks = self.different_months[self.prev_month.get_last_day_num().month]
            self.this_month = self.months[1]
            this_month_tasks = self.different_months[self.this_month.get_last_day_num().month]
        elif(len(self.months) == 1):
            self.this_month = self.months[0]
            this_month_tasks = self.different_months[self.this_month.get_last_day_num().month]
            
        prev_month_used_time = 0.
        if(self.prev_month is not None):
            for prev_month_task in prev_month_tasks:
                prev_month_used_time += prev_month_task.get_random_time()
        self.prev_month.set_support_task_time(self.prev_month.get_support_task_time() - prev_month_used_time)

        this_month_used_time = 0.
        if(self.this_month is not None):
            for this_month_task in this_month_tasks:
                this_month_used_time += this_month_task.get_random_time()

        self.this_month.set_support_task_time(self.this_month.get_support_task_time() - this_month_used_time)
