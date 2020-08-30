# TODO: Here will be all the calculation
import datetime
import calendar

from random import randrange 

def get_item_carousel_algorithm(range_start, range_end, step, task_entries):
    freq_coef_sum = 0.
    for task_entry in task_entries:
        freq_coef_sum += task_entry.get_freq_coef()
    
    chosen_number = randrange(int(freq_coef_sum))
    freq_coef_sum = 0.

    for task_entry in task_entries:
        freq_coef_sum += task_entry.get_freq_coef()
        if(chosen_number < freq_coef_sum):
            return task_entry
