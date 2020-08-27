from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import sys
from adding_data import DataAdder
import time

DB_NAME = "BugTracker.db"
WEBSITE = "https://bugtracker.allbau-software.de"
driver = webdriver.Firefox(executable_path=r'/Users/yaroslavoliinyk/Documents/YaroslavOliinyk___MacBook/Drivers/geckodriver')

class MainConstruction:
    def __init__(self):
        self.data_adder = DataAdder(DB_NAME, WEBSITE, driver)


if __name__ == "__main__":
    main_constr = MainConstruction()
    time.sleep(1000)
    driver.close()
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



