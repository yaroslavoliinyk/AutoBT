import sys
import time
import sqlite3
import logics

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from adding_data import DataAdder
from month import Month
from problem import Problem
from default_task import Default_Task

DB_NAME = "BugTracker.db"
WEBSITE = "https://bugtracker.allbau-software.de"
PREVIOUS_MONTH = Month('https://bugtracker.allbau-software.de/time_entries?utf8=%E2%9C%93&f%5B%5D=spent_on&op%5Bspent_on%5D=lm&f%5B%5D=user_id&op%5Buser_id%5D=%3D&v%5Buser_id%5D%5B%5D=me&f%5B%5D=&c%5B%5D=project&c%5B%5D=spent_on&c%5B%5D=user&c%5B%5D=activity&c%5B%5D=issue&c%5B%5D=comments&c%5B%5D=hours', False)
THIS_MONTH = Month('https://bugtracker.allbau-software.de/time_entries?utf8=%E2%9C%93&f%5B%5D=spent_on&op%5Bspent_on%5D=m&f%5B%5D=user_id&op%5Buser_id%5D=%3D&v%5Buser_id%5D%5B%5D=me&f%5B%5D=&c%5B%5D=project&c%5B%5D=spent_on&c%5B%5D=user&c%5B%5D=activity&c%5B%5D=issue&c%5B%5D=comments&c%5B%5D=hours', True)
driver = webdriver.Firefox(executable_path=r'/Users/yaroslavoliinyk/Documents/YaroslavOliinyk___MacBook/Drivers/geckodriver')
connection = sqlite3.connect(DB_NAME)

# ! THIS CHANGES MANUALLY BY USER:
INCLUDE_PREVIOUS_MONTH = True
INCLUDE_THIS_MONTH     = True

class MainConstruction:
    def __init__(self):
        #self.data_adder = DataAdder(DB_NAME, WEBSITE, driver, connection, PREVIOUS_MONTH, THIS_MONTH)
        self.conn = connection.cursor()
        self.problems_list = []
        self.months_list = []
        self.working_tasks_list = []
        self.fulfill_problems_list()
        self.fulfill_months_list()
        self.fulfill_working_tasks_list()
        self.avg_sp_time = logics.calculate_avg_sp_time(self.months_list, self.problems_list)
        Problem.AVG_SP_TIME = self.avg_sp_time
        self.fulfill_problems_with_tasks()

    def update_data(self):
        self.data_adder.update_datetimes()
        self.data_adder.update_months_hours()


    def fulfill_problems_list(self):
        command = "SELECT * FROM Tasks;"
        self.conn.execute(command)
        for entry in self.conn.fetchall():
            problem = Problem(entry[0], entry[1], entry[2])
            self.problems_list.append(problem)


    def fulfill_months_list(self):
        if(INCLUDE_PREVIOUS_MONTH):
            self.months_list.append(PREVIOUS_MONTH)
        if(INCLUDE_THIS_MONTH):
            self.months_list.append(THIS_MONTH)


    def fulfill_tasks_list(self):
        command = "SELECT * FROM WorkTaskTable;"
        self.conn.execute(command)
        for entry in self.conn.fetchall():
            work_task = Default_Task(entry[1], entry[2], entry[3], entry[4], True)
            self.working_tasks_list.append(work_task)


    def fulfill_problems_with_tasks(self):
        for problem in self.problems_list:
            while(not problem.is_more_than_sp_hours(Problem.AVG_SP_TIME)):
                random_task = logics.get_item_carousel_algorithm(self.working_tasks_list)
                new_random_task = Default_Task(random_task.get_name(), random_task.get_from_time(), 
                                    random_task.get_to_time(), random_task.get_freq_coef(), random_task.get_is_work_task())
                problem.add_task_and_time(new_random_task)

        print(self.problems_list)

        


if __name__ == "__main__":
    main_constr = MainConstruction()
    #main_constr.update_data()
    #time.sleep(1000)

    driver.close()
    connection.close()
    # dev branch for coding
    '''driver = webdriver.Firefox()
    driver.get("http://www.python.org")
    assert "Python" in driver.title
    elem = driver.find_element_by_name("q")
    elem.clear()
    elem.send_keys("pycon")
    elem.send_keys(Keys.RETURN)
    time.sleep(10)
    assert "No results found." not in driver.page_source
    driver.close()'''



