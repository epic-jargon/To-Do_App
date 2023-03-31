import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox, Text

import common


class TaskManager:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.frame.pack(fill='both', expand=True)

        # add style
        style = ttk.Style()

        # pick theme
        style.theme_use("default")

        # configure TreeView colors
        style.configure("Treeview",
                        background="#D3D3D3",
                        foreground="black",
                        rowheight=40,
                        fieldbackground="#D3D3D3",
                        font=(None, 24))

        # configure selcted color
        style.map("Treeview",
                  background=[("selected", "#347083")])

        # TreeView
        # Add scrollbar to TreeView
        self.tree_scroll = Scrollbar(self.frame)
        self.tree_scroll.pack(side=RIGHT, fill=Y)

        # Create TreeView
        self.my_tree = ttk.Treeview(self.frame, yscrollcommand=self.tree_scroll.set, selectmode="extended")
        self.my_tree.pack(fill='both', expand=True, padx=(10, 0))

        # Configure scrollbar
        self.tree_scroll.config(command=self.my_tree.yview)

        # Create columns
        self.my_tree["columns"] = ("ID", "Task",)

        # Format columns
        self.my_tree.column("#0", width=0, stretch=NO)
        self.my_tree.column("ID", anchor=W,stretch=NO, width=40)
        self.my_tree.column("Task", anchor=W, width=0)

        # Create headings
        self.my_tree.heading("#0", text="", anchor=W)
        self.my_tree.heading("ID", text="ID", anchor=W)
        self.my_tree.heading("Task", text="Task", anchor=W)

        # Create striped row tags
        self.my_tree.tag_configure("odd_row", background="white")
        self.my_tree.tag_configure("even_row", background="lightblue")

        # Entry boxes
        self.data_frame = tk.Frame(master)
        self.data_frame.pack(fill="x")

        self.task_name_entry = Text(self.data_frame, height=1, font=('Ariel', 32))
        self.task_name_entry.pack()

        # Buttons
        self.button_frame = tk.Frame(self.master)
        self.button_frame.pack(fill="x")

        self.add_button = Button(self.button_frame, text="Add", command=self.add_record)
        self.add_button.grid(row=0, column=0, padx=10, pady=10)

        self.update_button = Button(self.button_frame, text="Update", command=self.update_record)
        self.update_button.grid(row=0, column=1, padx=10, pady=10)

        self.clear_button = Button(self.button_frame, text="Clear", command=self.clear_entries)
        self.clear_button.grid(row=0, column=2, padx=10, pady=10)

        self.remove_selected_button = Button(self.button_frame, text="Remove selected", command=self.delete_selected)
        self.remove_selected_button.grid(row=0, column=3, padx=10, pady=10)

        # Bindings
        self.my_tree.bind("<ButtonRelease-1>", self.select_record)

        # run to query database and fill table
        self.query_database()

    # form table
    def query_database(self):
        records = common.query_database("SELECT rowid, * FROM tasks")

    #add data to screen
        count = 0
        for record in records:
            if count % 2 == 0:
                self.my_tree.insert(parent="", index="end", iid=count, text="",
                                    values=(record[0], record[1]),
                                    tags="even_row")
            else:
                self.my_tree.insert(parent="", index="end", iid=count, text="",
                                    values=(record[0], record[1]),
                                    tags="odd_row")
            count += 1

    # clear entry boxes
    def clear_entries(self):
        self.task_name_entry.delete("1.0", END)

    # select record
    def select_record(self, e):
        self.clear_entries()

        # grab record number
        selected = self.my_tree.focus()
        # grab record values
        values = self.my_tree.item(selected, "values")

        self.task_name_entry.insert("1.0", values[1])

    # update record
    def update_record(self):
        # get record number
        selected = self.my_tree.focus()
        record_id = self.my_tree.item(selected, "values")[0]

        # update record
        self.my_tree.item(selected, text="", values=(record_id, self.task_name_entry.get('1.0', END)))
        query = f"""UPDATE tasks SET
                    task = '{self.task_name_entry.get('1.0', END)}' 
                    WHERE oid = {record_id}"""
        common.query_database(query)

        # clear entries
        self.clear_entries()

    # add new record to database
    def add_record(self):
        # inset new entry
        common.query_database(f"""INSERT INTO tasks VALUES ("{self.task_name_entry.get('1.0', END)}")""")

        # clear entries
        self.clear_entries()

        # clear TreeView
        self.my_tree.delete(*self.my_tree.get_children())

        # reload TreeView
        self.query_database()

    # Remove entry
    def delete_selected(self):
        x = self.my_tree.selection()

        # list of ids to delete
        ids_to_delete = []

        # add selection to delete
        for record in x:
            ids_to_delete.append(self.my_tree.item(record, "values")[0])

        # delete row from database
        common.query_database_many("DELETE from tasks WHERE oid= ?", ids_to_delete)

        # reset table
        self.my_tree.delete(*self.my_tree.get_children())
        self.query_database()
        # clear entries
        self.clear_entries()

