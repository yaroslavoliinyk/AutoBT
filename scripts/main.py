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
from support_problem import SupportProblem
from webdriver_manager.chrome import ChromeDriverManager


DB_NAME = "BugTracker.db"
WEBSITE = "https://bugtracker.allbau-software.de"
PREVIOUS_MONTH = Month('https://bugtracker.allbau-software.de/time_entries?utf8=%E2%9C%93&f%5B%5D=spent_on&op%5Bspent_on%5D=lm&f%5B%5D=user_id&op%5Buser_id%5D=%3D&v%5Buser_id%5D%5B%5D=me&f%5B%5D=&c%5B%5D=project&c%5B%5D=spent_on&c%5B%5D=user&c%5B%5D=activity&c%5B%5D=issue&c%5B%5D=comments&c%5B%5D=hours', False)
THIS_MONTH = Month('https://bugtracker.allbau-software.de/time_entries?utf8=%E2%9C%93&f%5B%5D=spent_on&op%5Bspent_on%5D=m&f%5B%5D=user_id&op%5Buser_id%5D=%3D&v%5Buser_id%5D%5B%5D=me&f%5B%5D=&c%5B%5D=project&c%5B%5D=spent_on&c%5B%5D=user&c%5B%5D=activity&c%5B%5D=issue&c%5B%5D=comments&c%5B%5D=hours', True)
WRITE_WEBSITE = "https://bugtracker.allbau-software.de/issues/7793/time_entries/new"
driver = webdriver.Chrome(ChromeDriverManager().install())
connection = sqlite3.connect(DB_NAME)

# ! THIS CHANGES MANUALLY BY USER:
INCLUDE_PREVIOUS_MONTH = False
INCLUDE_THIS_MONTH     = True

class MainConstruction:
    def __init__(self):
        self.data_adder = DataAdder(DB_NAME, WEBSITE, driver, connection, PREVIOUS_MONTH, THIS_MONTH)
        self.conn = connection.cursor()
        self.problems_list = []
        self.months_list = []
        self.working_tasks_list = []
        # Will be assigned on fulfill_support...
        self.support_problem = None

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
                                    random_task.get_to_time(), random_task.get_freq_coef(), random_task.get_is_work_task())
                problem.add_task_and_time(new_random_task)


    def fulfill_support_problem_with_tasks(self):
        self.support_problem = SupportProblem(self.months_list)
        
        command = "SELECT * FROM SupportTaskTable;"
        self.conn.execute(command)
        entries = self.conn.fetchall()
        
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
        for month in self.months_list:
            remained_support_task_time = month.get_support_task_time()
            while(remained_support_task_time > 0):
                random_support_task = logics.get_item_carousel_algorithm(self.support_problem_list)
                new_random_support_task = Default_Task(random_support_task.get_name(), random_support_task.get_from_time(), 
                                    random_support_task.get_to_time(), random_support_task.get_freq_coef(), random_support_task.get_is_work_task())
                self.support_problem.add_task_and_time(month.get_month_num(), new_random_support_task)
                remained_support_task_time -= new_random_support_task.get_random_time()
        
        print("SUPPORT TASKS")
        print("_____________")
        print("_____________")
        #print(self.support_problem.get_support_task_list())
        print("_____________")
        print("_____________")
        

    def __make_tasks_from_support_problem_list(self, support_problem_list):
        support_task_list = []
        for support_problem in support_problem_list:
            task = Default_Task(support_problem[1], support_problem[2], support_problem[3], support_problem[4], False)
            support_task_list.append(task)
        
        return support_task_list


    def write_to_bugtracker(self):
        driver.get(WRITE_WEBSITE)
        # WRITING SUPPORT TASK
        '''for task in self.support_problem.get_support_task_list():
            print("writing " + task.__str__())
            if(isinstance(task.get_date(), list)):
                for one_date in task.get_date():
                    self.__write_task(SupportProblem.PROBLEM_ID, one_date, task.get_random_time(), task.get_name(), True)
            else:
                self.__write_task(SupportProblem.PROBLEM_ID, task.get_date(), task.get_random_time(), task.get_name(), True)'''        

        time.sleep(5)
        print("PROBLEM TASKS")
        for problem in self.problems_list:
            for task_list in list(problem.get_task_dict().values()):
                for task in task_list:
                    print("writing " + task.__str__())
        # WRITING PROBLEMS TASKS
        for problem in self.problems_list:
            for task_list in list(problem.get_task_dict().values()):
                for task in task_list:
                    print("writing " + task.__str__())
                    self.__write_task(problem.get_problem_num(), task.get_date(), task.get_random_time(), task.get_name(), False)
                    time.sleep(1)

    
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





if __name__ == "__main__":
    main_constr = MainConstruction()
    main_constr.update_data()
    #time.sleep(1000)
    main_constr.fulfill_problems_list()
    main_constr.fulfill_months_list()
    main_constr.fulfill_working_tasks_list()
    avg_sp_time = logics.calculate_avg_sp_time(main_constr.months_list, main_constr.problems_list)
    Problem.AVG_SP_TIME = avg_sp_time
    main_constr.fulfill_problems_with_tasks()
    for month in main_constr.months_list:
        print("MONTH TIME")
        print("Month from: ", month.get_start_day_num())
        print("Month to: ", month.get_last_day_num())
        print(month.get_work_time_a_day())
        print(month.get_hours())
    main_constr.fulfill_support_problem_with_tasks()
    main_constr.write_to_bugtracker()
    time.sleep(300)
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



