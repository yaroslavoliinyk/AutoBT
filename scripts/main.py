import sys
import time
import sqlite3

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from adding_data import DataAdder

DB_NAME = "BugTracker.db"
WEBSITE = "https://bugtracker.allbau-software.de"
PREVIOUS_MONTH = True
THIS_MONTH = True
driver = webdriver.Firefox(executable_path=r'/Users/yaroslavoliinyk/Documents/YaroslavOliinyk___MacBook/Drivers/geckodriver')
connection = sqlite3.connect(DB_NAME)

class MainConstruction:
    def __init__(self):
        self.data_adder = DataAdder(DB_NAME, WEBSITE, driver, connection)
        

    def update_datetimes_for_tasks(self):
        self.data_adder.update_datetimes()

if __name__ == "__main__":
    main_constr = MainConstruction()
    main_constr.update_datetimes_for_tasks()
    time.sleep(1000)
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



