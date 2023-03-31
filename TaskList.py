import tkinter as tk
from tkinter import *

import common


class TaskList:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.frame.pack(fill='both', expand=True)

        self.dynamic_tasks = []
        self.fill_tasks()

    @staticmethod
    def task_manager_button():
        top = tk.Toplevel()
        top.title("Task Manager")

    def fill_tasks(self):
        records = common.query_database("SELECT rowid, * FROM tasks")
        print(records)

        for record in range(len(records)):
            fm = Frame(self.frame, bd=1)
            self.dynamic_tasks.append(fm)
            fm.pack(anchor=W)
            Label(fm, text=records[record][1]).pack(anchor=W)
            btn = Button(fm, text=f"X", command=lambda i=record: self.remove_task(i))
            btn.pack(anchor=E)

    def remove_task(self, item):
        self.dynamic_tasks[item].destroy()
        print(item)