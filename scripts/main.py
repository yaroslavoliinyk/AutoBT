import sys
import time
import sqlite3
import logics
import datetime

from random import randrange
from selenium.common.exceptions import NoSuchElementException
from datetime import date, timedelta
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from problem import Problem
from default_task import Default_Task
from support_problem import SupportProblem
from webdriver_manager.chrome import ChromeDriverManager


DB_NAME = "BugTracker.db"
WEBSITE = "https://bugtracker.allbau-software.de"
WRITE_WEBSITE = "https://bugtracker.allbau-software.de/issues/7793/time_entries/new"
AUTH_TABLE = "Authentication"
# Start and end dates for filling the fields
START_DATE = None
END_DATE = None
DATE_LIST = list()
# Number of hours of work
AVG_HOUR_PER_DAY = 6.5
WORK_COEF = 0.75
SUPPORT_COEF = 1.-WORK_COEF

driver = webdriver.Chrome(ChromeDriverManager().install())
connection = sqlite3.connect(DB_NAME)


class MainConstruction:

    def __init__(self):
        self.conn = connection.cursor()
        self.problems_list = []
        self.working_tasks_list = []
        # Will be assigned on fulfill_support...
        self.support_problem = None


    def fulfill_problems_list(self):
        command = "SELECT * FROM Tasks;"
        self.conn.execute(command)
        all_problems = self.conn.fetchall()
        for entry in all_problems:
            problem = Problem(entry[0], entry[1], entry[2])
            self.problems_list.append(problem)


    def fulfill_working_tasks_list(self):
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
                                    random_task.get_to_time(), random_task.get_freq_coef(), random_task.get_is_work_task(), str(problem.get_problem_num()))
                problem.add_task(new_random_task)
            print("!!! PROBLEM !!!", problem.__str__())


    def fulfill_support_problem_with_tasks(self, date_list):
        support_time = len(date_list) * AVG_HOUR_PER_DAY * SUPPORT_COEF
        self.support_problem = SupportProblem(date_list, support_time)
        
        command = "SELECT * FROM SupportTaskTable;"
        self.conn.execute(command)
        entries = self.conn.fetchall()
        print("ENTRIES", entries)
        # Special cases of Support Task
        daily = Default_Task(entries[0][1], entries[0][2], entries[0][3], entries[0][4], False)
        tech_improvement = Default_Task(entries[3][1], entries[3][2], entries[3][3], entries[3][4], False)
        review_plan_retro = Default_Task(entries[9][1], entries[9][2], entries[9][3], entries[9][4], False)
        
        self.support_problem.fulfill_with_special_tasks(daily, tech_improvement, review_plan_retro)
        # Remove daily, tech_improvement and revoew_plan_retro from support tasks
        entries.pop(0)
        entries.pop(3)
        entries.pop(9)

        self.support_problem_list = entries
        self.support_problem_list = self.__make_tasks_from_support_problem_list(self.support_problem_list)
        print(self.support_problem_list)
        while(self.support_problem.get_support_time() > 0.):
            random_support_task = logics.get_item_carousel_algorithm(self.support_problem_list)
            new_random_support_task = Default_Task(random_support_task.get_name(), random_support_task.get_from_time(), 
                                    random_support_task.get_to_time(), random_support_task.get_freq_coef(), random_support_task.get_is_work_task())
            
            random_date_index = randrange(len(DATE_LIST))
            # Here's where support time subtracts
            self.support_problem.add_task_and_time(new_random_support_task, DATE_LIST[random_date_index])


    # Sort ascendingly problems by data
    def sort_problems_list(self):
        self.problems_list.sort(key=lambda problem: problem.get_date())


    def calculate_avg_sp_time(self, date_list, problems_list):
        working_days_number = len(DATE_LIST)
        sp_number = Problem.get_total_sps(problems_list)
        working_days_hours = working_days_number * AVG_HOUR_PER_DAY * WORK_COEF
        avg_sp_time = working_days_hours / sp_number
        print("AVG SP TIME", avg_sp_time)
        
        return avg_sp_time


    def sign_in(self, website_page, auth_table):
        try:
            print("Start")
            login = self.conn.execute("SELECT LOGIN FROM "+auth_table+";")
            login = self.conn.fetchone()
            password = self.conn.execute("SELECT PASSWORD FROM "+auth_table+";")
            password = self.conn.fetchone()
            print(login, password)
            driver.get(website_page)
            elem = driver.find_element_by_name("username")
            elem.clear()
            elem.send_keys(login)

            elem = driver.find_element_by_name("password")
            elem.clear()
            elem.send_keys(password)
            
            elem = driver.find_element_by_name("login")
            elem.send_keys(Keys.RETURN)
            time.sleep(0.5)
            # Was not logged in
            return False
        except NoSuchElementException as e:
            # Was logged in
            return True



    def write_to_bugtracker(self):
        driver.get(WRITE_WEBSITE)
        # WRITING SUPPORT TASK
        for task in self.support_problem.get_support_task_list():
            print("writing " + task.__str__())
            if(isinstance(task.get_date(), list)):
                for one_date in task.get_date():
                    self.__write_task(SupportProblem.PROBLEM_ID, one_date, task.get_random_time(), task.get_name(), True)
            else:
                self.__write_task(SupportProblem.PROBLEM_ID, task.get_date(), task.get_random_time(), task.get_name(), True)   

        time.sleep(5)

         # WRITING PROBLEM TASKS
        print("PROBLEM TASKS")
        all_tasks = list()
        for problem in main_constr.problems_list:
            all_tasks.extend(problem.get_task_list())
        
        tasks_a_day = len(all_tasks) // len(DATE_LIST)
        
        for one_date in DATE_LIST:
            for _ in range(tasks_a_day):
                task = all_tasks.pop(0)
                print("writing " + task.__str__())
                self.__write_task(task.get_problem_number(), one_date, task.get_random_time(), task.get_name(), False)
                time.sleep(1)

        
    def __make_tasks_from_support_problem_list(self, support_problem_list):
        support_task_list = []
        for support_problem in support_problem_list:
            task = Default_Task(support_problem[1], support_problem[2], support_problem[3], support_problem[4], False)
            support_task_list.append(task)
        
        return support_task_list


    def __write_task(self, problem_id, task_date, task_time, task_name, is_support_task_problem):
        # Write number of the task
        elem = driver.find_element_by_class_name("ui-autocomplete-input")
        elem.clear()
        time.sleep(0.25)
        elem.send_keys(str(problem_id))
        print(str(problem_id))
        time.sleep(1)

        # Write date
        driver.execute_script('document.getElementById("time_entry_spent_on").removeAttribute("readonly")')
        elem = driver.find_element_by_xpath("//form//input[@name='time_entry[spent_on]']")
        elem.clear()
        time.sleep(0.25)
        str_date = ""
        if(len(str(task_date.day)) < 2):
            task_date_day = "0" + str(task_date.day)
        else:
            task_date_day = str(task_date.day)

        if(len(str(task_date.month)) < 2):
            task_date_month = "0" + str(task_date.month)
        else:
            task_date_month = str(task_date.month)

        str_date += str(task_date_day)
        str_date += str(task_date_month)
        str_date += str(task_date.year)

        elem.send_keys(str_date)
        print(str_date)
        time.sleep(1)

        # Hours number
        elem = driver.find_element_by_id("time_entry_hours")
        elem.clear()
        time.sleep(0.25)
        elem.send_keys(str(task_time))
        print(str(task_time))
        time.sleep(1)

        # Write task name
        elem = driver.find_element_by_name("time_entry[comments]")
        elem.clear()
        time.sleep(0.25)
        elem.send_keys(task_name)
        print(task_name)
        time.sleep(1)

        # Choose Developement from Combobox
        elem = driver.find_element_by_xpath("//select[@name='time_entry[activity_id]']")
        all_options = elem.find_elements_by_tag_name("option")
        if(is_support_task_problem):
            all_options[3].click()
        else:
            all_options[0].click()
        time.sleep(1)

        # Clicking next to enter next value
        elem = driver.find_element_by_name("continue")
        elem.click()


def fulfill_date_list():
    elapsed_time = END_DATE - START_DATE
    days_delta = elapsed_time.days
    for day_dt in range(days_delta):
        DATE_LIST.append(START_DATE+timedelta(days=day_dt))
    # Only workdays
    dates_list = list()
    dates_list.extend(DATE_LIST)
    dates_list = list(filter(lambda date_day: date_day.weekday()<6, DATE_LIST))
    DATE_LIST.clear()
    DATE_LIST.extend(dates_list)





if __name__ == "__main__":
    # Input format
    # 2020-11-30
    # 2020-01-21
    #start_dt = input()
    #end_dt   = input()
    
    START_DATE = date.fromisoformat("2020-09-01")
    END_DATE = date.fromisoformat("2020-09-12")
    # Only workdays
    fulfill_date_list()

    print(DATE_LIST)

    main_constr = MainConstruction()

    main_constr.fulfill_problems_list()
    # Print all problems
    for problem in main_constr.problems_list:
        print(problem.__str__())
        print("\n")

    main_constr.fulfill_working_tasks_list()
    for work_task in main_constr.working_tasks_list:
        print(work_task)
        print("------------\n")
    
    avg_sp_time = main_constr.calculate_avg_sp_time(DATE_LIST, main_constr.problems_list)
    Problem.AVG_SP_TIME = avg_sp_time
    # Here is OK.
    main_constr.fulfill_problems_with_tasks()
    
    # OPTIONAL!!!! It can be sorted or not!
    main_constr.sort_problems_list()
    
    main_constr.fulfill_support_problem_with_tasks(DATE_LIST)

    print(main_constr.support_problem)
    for sup_task in main_constr.support_problem.get_support_task_list():
        print(sup_task.__str__())


    # ! Here is incorrect. Need to make new logics
    # Problems: contain tasks with no concrete dates to write to program.
    # Support Problem: contains everything needed for writing to BT
    main_constr.sign_in(WEBSITE, AUTH_TABLE)
    main_constr.write_to_bugtracker()
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



