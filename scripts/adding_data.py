import datetime
import sqlite3

class DataAdder:
    def __init__(self, db_name):
        self.db_name = db_name
        self.tasks = []
        self.__update_datetimes()
        

    def __update_datetimes(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("SELECT * FROM Tasks;")
        tasks_table = c.fetchall()
        self.tasks.extend(self.__get_tasks(tasks_table))
        print(self.tasks)

    def __get_tasks(self, tasks_table):
        tasks = []
        for task in tasks_table:
            tasks.append(task[0])
        return tasks

    