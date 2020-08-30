import sys
import time
import sqlite3

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from adding_data import DataAdder
from month import Month

DB_NAME = "BugTracker.db"
WEBSITE = "https://bugtracker.allbau-software.de"
PREVIOUS_MONTH = Month('https://bugtracker.allbau-software.de/time_entries?utf8=%E2%9C%93&f%5B%5D=spent_on&op%5Bspent_on%5D=lm&f%5B%5D=user_id&op%5Buser_id%5D=%3D&v%5Buser_id%5D%5B%5D=me&f%5B%5D=&c%5B%5D=project&c%5B%5D=spent_on&c%5B%5D=user&c%5B%5D=activity&c%5B%5D=issue&c%5B%5D=comments&c%5B%5D=hours', False)
THIS_MONTH = Month('https://bugtracker.allbau-software.de/time_entries?utf8=%E2%9C%93&f%5B%5D=spent_on&op%5Bspent_on%5D=m&f%5B%5D=user_id&op%5Buser_id%5D=%3D&v%5Buser_id%5D%5B%5D=me&f%5B%5D=&c%5B%5D=project&c%5B%5D=spent_on&c%5B%5D=user&c%5B%5D=activity&c%5B%5D=issue&c%5B%5D=comments&c%5B%5D=hours', True)
driver = webdriver.Firefox(executable_path=r'/Users/yaroslavoliinyk/Documents/YaroslavOliinyk___MacBook/Drivers/geckodriver')
connection = sqlite3.connect(DB_NAME)

class MainConstruction:
    def __init__(self):
        self.data_adder = DataAdder(DB_NAME, WEBSITE, driver, connection, PREVIOUS_MONTH, THIS_MONTH)
        

    def update_data(self):
        self.data_adder.update_datetimes()
        self.data_adder.update_months_hours()


if __name__ == "__main__":
    main_constr = MainConstruction()
    main_constr.update_data()
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



