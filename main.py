import tkinter as tk
from tkinter import *
from tkinter import ttk

import TaskManager
import common
import TaskList


class MainApplication:
    def __init__(self, master):
        self.master = master
    # Menu
        app_menu = tk.Menu(master)
        master.config(menu=app_menu)

        file_menu = tk.Menu(app_menu, tearoff=0)
        app_menu.add_cascade(label="File", menu=file_menu)
        # file_menu.add_command(label="Task manager", command=self.task_manager_button)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=master.quit)

        root.grid_columnconfigure(0, weight=1)
        root.grid_rowconfigure(1, weight=1)

    # Contents
        # task_list = TaskList.TaskList(master)
        task_manager = TaskManager.TaskManager(master)

        create_table()


# create table if it doesnt exist
def create_table():
    common.query_database("""CREATE TABLE if not exists tasks (
                    task text)
                    """)
    # common.query_database("INSERT INTO tasks (task) VALUES ('task')")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("To-Do App")
    root.geometry("500x600")
    app = MainApplication(root)
    root.mainloop()


