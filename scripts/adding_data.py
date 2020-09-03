import datetime
import time

from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

TASKS_TABLE = "Tasks"
AUTH_TABLE = "Authentication"


class DataAdder:
    

    def __init__(self, db_name, website_name, driver, db_connection, prev_month, this_month):
        self.website_name = website_name
        self.tasks = []
        self.driver = driver
        self.connection = db_connection
        self.conn = self.connection.cursor()
        self.prev_month = prev_month
        self.this_month = this_month


    def update_datetimes(self):
        self.conn.execute("SELECT * FROM Tasks;")
        tasks_table = self.conn.fetchall()
        self.tasks.extend(self.__get_tasks(tasks_table))
        if self.__sign_in(self.website_name, AUTH_TABLE):
            print("User was already logged in")
        else:
            print("Logging in...")
        for task_id in self.tasks:
            self.__update_task_dt(task_id, TASKS_TABLE)
        

    def update_months_hours(self):
        self.__make_months_hours(self.prev_month)
        self.__make_months_hours(self.this_month)
        print(self.prev_month.get_hours())
        print(self.this_month.get_hours())
        print(self.prev_month.get_last_commit())
        print(self.this_month.get_last_commit())


    def __make_months_hours(self, month):
        #! Not correct. Also applies for current month.
        #! Since it's not obligatory to start new month from date 1
        # Corrected above error
        # ? Hard code
        # ? self.driver.get(month.get_link())
        # ? elem = self.driver.find_element_by_class_name("hours")
        # ? month.set_hours(float(elem.text))
        if(not month.get_current_month()):
            month.set_hours(87.)
        else:
            month.set_hours(0.)

        try: 
            elem = self.driver.find_element_by_class_name("spent_on")
            month.set_last_commit(datetime.datetime.strptime(elem.text, '%Y-%m-%d'))
        except NoSuchElementException as e:
            month.set_last_commit(None)
                


    def __update_task_dt(self, task_id, task_tb):
        website_page = self.website_name + "/issues/" + str(task_id)
        self.driver.get(website_page)
        time.sleep(0.5)
        elems = self.driver.find_elements_by_tag_name("a")
        for elem in elems:
            if(elem.get_property("title") != ""):
                time_property = elem.get_property("title")
                break
        command = "UPDATE "+task_tb+" SET created="+"'"+time_property+"'"+" WHERE task_id="+str(task_id)+";"
        print(command)
        self.conn.execute(command)
        self.connection.commit()
        print(time_property)       
        print(type(elems))


    def __sign_in(self, website_page, auth_table):
        try:
            print("Start")
            login = self.conn.execute("SELECT LOGIN FROM "+auth_table+";")
            login = self.conn.fetchone()
            password = self.conn.execute("SELECT PASSWORD FROM "+auth_table+";")
            password = self.conn.fetchone()
            print(login, password)
            self.driver.get(website_page)
            elem = self.driver.find_element_by_name("username")
            elem.clear()
            elem.send_keys(login)

            elem = self.driver.find_element_by_name("password")
            elem.clear()
            elem.send_keys(password)
            
            elem = self.driver.find_element_by_name("login")
            elem.send_keys(Keys.RETURN)
            time.sleep(0.5)
            # Was not logged in
            return False
        except NoSuchElementException as e:
            # Was logged in
            return True
        

    def __get_tasks(self, tasks_table):
        tasks = []
        for task in tasks_table:
            tasks.append(task[0])
        return tasks
