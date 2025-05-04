import tkinter as tk
from tkinter import ttk
import task_manager_db as db
from task_manager_db import *
from datetime import datetime
import tkinter.messagebox as messagebox


class TaskManagerGUI:

    def __init__(self, root):
        self.root = root
        #self.register_page()
        self.login_page()
        db.create_db()
        self.db_user_columns=['id', 'username', 'password']
        self.db_task_columns=['id', 'user_id', 'description', 'date', 'category', 'priority', 'status']
        self.tree = None
        self.current_user = None
        self.root.title("Task Manager")

    def register_user(self, username, password):
        if username and password:
            user = db.session.query(User).filter_by(username=username).first()
            if user:
                messagebox.showerror("Invalid Input","Username already exists")
            else:    
                user = db.add_user(username, password)
                for widget in self.root.winfo_children():
                    widget.destroy()
                self.login_page()
        else:
            messagebox.showerror("Invalid Input","Empty Fields")
    
    def login(self, username, password):
        if username and password:
            user = db.login(username, password)    
            if user:
                for widget in self.root.winfo_children():
                    widget.destroy()
                self.current_user = user
                self.add_task_page(user)
            else:
                messagebox.showerror("Invalid Input","Wrong username and/or password")
        else:
            messagebox.showerror("Invalid Input","Empty Fields")

    def add_task(self, description, date, category, priority, status):
        if all([description, date, category, priority, status]):
            try:
            # Validate date format
                date = datetime.strptime(date, "%Y-%m-%d").date()
            except ValueError:
                messagebox.showerror("Invalid Input", "Date must be in YYYY-MM-DD format.")
            db.add_task(self.current_user.id, description, date, category, priority, status)
        else:
            messagebox.showerror("Invalid Input", "Empty Fields")
        
    def tree_view(self):
        if self.tree:
            self.tree.destroy()
        self.tree = ttk.Treeview(self.root, columns=self.db_user_columns, show='headings')

        for col in self.db_user_columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        for user in db.get_users():
            self.tree.insert("", tk.END, values=(user.id, user.username, user.password))

        self.tree.pack(padx=10, pady=10)

    def user_task_tree_view(self):
        if self.tree:
            self.tree.destroy()
        self.tree = ttk.Treeview(self.root, columns=self.db_task_columns, show='headings')

        for col in self.db_task_columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        for task in db.get_tasks_user_id(self.current_user.id):
            self.tree.insert("", tk.END, values=(task.id, task.user_id, task.description, task.date, task.category, task.priority, task.status))
        
        self.tree.pack(padx=10, pady=10)

    def login_page(self):
        label = ttk.Label(self.root, text="Login")
        label.pack(padx=20, pady=20)

        
        username_field = ttk.Label(self.root, text="username")
        username_field.pack(padx=20, pady=20)
        username_value = tk.StringVar()
        username_entry = ttk.Entry(self.root, textvariable=username_value, width = 30)
        username_entry.pack(padx=10, pady=10)
        
        password_field = ttk.Label(self.root, text="password")
        password_field.pack(padx=20, pady=20)
        password_value = tk.StringVar()
        password_entry = ttk.Entry(self.root, textvariable=password_value, width = 30)
        password_entry.pack(padx=10, pady=10)
        
        button = ttk.Button(self.root, text="Sign in", command=lambda: self.login(username_entry.get(), password_entry.get()))
        button.pack(padx=10, pady=10) 

        button2 = ttk.Button(self.root, text="Users", command = lambda: self.tree_view())
        button2.pack(padx=10, pady=10) 
        
    def register_page(self):
        label = ttk.Label(self.root, text="Register")
        label.pack(padx=20, pady=20)

        
        username_field = ttk.Label(self.root, text="username")
        username_field.pack(padx=20, pady=20)
        username_value = tk.StringVar()
        username_entry = ttk.Entry(self.root, textvariable=username_value, width = 30)
        username_entry.pack(padx=10, pady=10)
        
        password_field = ttk.Label(self.root, text="password")
        password_field.pack(padx=20, pady=20)
        password_value = tk.StringVar()
        password_entry = ttk.Entry(self.root, textvariable=password_value, width = 30)
        password_entry.pack(padx=10, pady=10)
        
        button = ttk.Button(self.root, text="Sign Up", command=lambda: self.register_user(username_entry.get(), password_entry.get()))
        button.pack(padx=10, pady=10) 

        button2 = ttk.Button(self.root, text="My Book Collection", command = lambda: self.tree_view())
        button2.pack(padx=10, pady=10) 

        button3 = ttk.Button(self.root, text="Delete", command=lambda: db.delete_all_users())
        button3.pack(padx=10, pady=10) 

    def add_task_page(self, user):
        
        label = ttk.Label(self.root, text="Username: " + str(user.username))
        label.pack(padx=20, pady=20)

        label = ttk.Label(self.root, text="Password: " + str(user.password))
        label.pack(padx=20, pady=20)

        description_field = ttk.Label(self.root, text="description")
        description_field.pack(padx=20, pady=20)
        description_value = tk.StringVar()
        description_entry = ttk.Entry(self.root, textvariable=description_value, width = 30)
        description_entry.pack(padx=10, pady=10)
        
        date_field = ttk.Label(self.root, text="date (YYYY-MM-DD)")
        date_field.pack(padx=20, pady=20)
        date_value = tk.StringVar()
        date_entry = ttk.Entry(self.root, textvariable=date_value, width = 30)
        date_entry.pack(padx=10, pady=10)

        category_field = ttk.Label(self.root, text="category")
        category_field.pack(padx=20, pady=20)
        category_value = tk.StringVar()
        category_entry = ttk.Entry(self.root, textvariable=category_value, width = 30)
        category_entry.pack(padx=10, pady=10)

        priority_field = ttk.Label(self.root, text="priority")
        priority_field.pack(padx=20, pady=20)
        priority_value = tk.IntVar()
        priority_entry = ttk.Entry(self.root, textvariable=priority_value, width = 30)
        priority_entry.pack(padx=10, pady=10)

        status_field = ttk.Label(self.root, text="status")
        status_field.pack(padx=20, pady=20)
        status_value = tk.StringVar()
        status_entry = ttk.Entry(self.root, textvariable=status_value, width = 30)
        status_entry.pack(padx=10, pady=10)
        
        button = ttk.Button(self.root, text="Add", command=lambda: self.add_task(description_value.get(), date_value.get(), category_value.get(), priority_value.get(), status_value.get()))
        button.pack(padx=10, pady=10) 

        button2 = ttk.Button(self.root, text="View Tasks", command=lambda: self.user_task_tree_view())
        button2.pack(padx=10, pady=10) 

if __name__ == "__main__":
    root = tk.Tk()
    bookApplication = TaskManagerGUI(root)
    root.mainloop()