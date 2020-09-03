from random import randrange
import datetime

class Default_Task:
    
    def __init__(self, name, from_time, to_time, freq_coef, is_work_task):
        self.name = name
        self.from_time = from_time
        self.to_time = to_time
        # how frequently we meet the task
        self.freq_coef = freq_coef
        # whether it's a work task or support task
        self.is_work_task = is_work_task
        # each task can have a date of implementation
        self.date = None
        # The random time estimated for the concrete task
        self.random_time = self.__get_inner_random_time()

    #------- These two values are filled later on --------

    def set_random_time(self, random_time):
        self.random_time = random_time


    def get_random_time(self):
        return self.random_time


    def set_date(self, date):
        self.date = date


    def get_date(self):
        return self.date

    #-----------------------------------------------------    

    def get_name(self):
        return self.name

    
    def get_from_time(self):
        return self.from_time


    def get_to_time(self):
        return self.to_time


    def get_is_work_task(self):
        return self.is_work_task

    def __get_inner_random_time(self):
        delta_range = self.get_to_time() - self.get_from_time()
        # The same as divide by 0.25, since all the time has to be dividable by 0.25
        delta_range *= 4
        delta_range = int(delta_range)
        if(delta_range != 0):
            random_range_time = randrange(delta_range)
            # Translate again into time
            random_range_time *= 0.25
        else:
            random_range_time = 0
        
        return self.get_from_time() + random_range_time
        

    def get_freq_coef(self):
        return self.freq_coef

    
    def __str__(self):
        if(not isinstance(self.date, datetime.date)):
            print("HUINIA SOBACHA!!!!")
            print(type(self.date))
        return "Task: " + self.name + "; time: " + str(self.random_time) + "; freq_coef: " + str(self.freq_coef) + "; date: " + str(self.date) + " ."