# TODO: Here will be all the calculation
import datetime
import calendar
import time

from random import randrange 
from problem import Problem
from month import Month

def get_item_carousel_algorithm(task_entries):
    freq_coef_sum = 0.
    for task_entry in task_entries:
        freq_coef_sum += task_entry.get_freq_coef()
    
    chosen_number = randrange(int(freq_coef_sum))
    freq_coef_sum = 0.

    for task_entry in task_entries:
        freq_coef_sum += task_entry.get_freq_coef()
        if(chosen_number < freq_coef_sum):
            return task_entry

    raise Exception("Not supposed to go here!!!")


def calculate_avg_sp_time(date_list, problems_list):
        '''working_days_number = 0
        for month in months_list:
            wd_number, _ = month.get_working_days_number()
            working_days_number += wd_number

        sp_number = Problem.get_total_sps(problems_list)
        # Formula to calculate how many hours was delegated to developing throught the given perioud
        working_days_hours = working_days_number * Month.AVG_HOUR_PER_DAY * Month.WORK_COEF
        avg_sp_time = working_days_hours / sp_number
        return avg_sp_time'''

        working_days_number = Problem.get_working_days_num_in_range(date_list[0], date_list[len(date_list)-1])
        print("working_days_number", working_days_number)
        sp_number = Problem.get_total_sps(problems_list)
        print("sp_number", sp_number)
        working_days_hours = working_days_number * Month.AVG_HOUR_PER_DAY * Month.WORK_COEF
        print("working_days_hours", working_days_hours)
        avg_sp_time = working_days_hours / sp_number
        print("avg_sp_time", avg_sp_time)

        return avg_sp_time