import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
from task_manager_db import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import StringVar
from collections import Counter
from tkcalendar import Calendar
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

database_filename = "task_management.db"
engine = create_engine(f"sqlite:///{database_filename}", echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

def init_db():
    """Initialize the database and create all tables"""
    Base.metadata.create_all(bind=engine)


class TaskManagerGUI:

    def __init__(self, root):
        self.root = root
        self.root.title("Taskify - Task Manager")
        self.root.geometry("1000x800")
        self.root.config(bg="white")
        self.current_user = None
        self.tree = None
        self.filtered_status = "All"
        self.filtered_priority = "All"
        self.login_page()

    def login_page(self):
        """Login page of the application. Displays the login form."""
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = ttk.Frame(self.root)
        frame.pack(pady=100)

        label = ttk.Label(frame, text="Taskify", font=("Open Sans", 24, "bold"))
        label.pack(pady=20)

        username_label = ttk.Label(frame, text="Username", font=("Open Sans", 12))
        username_label.pack(padx=10, pady=5)

        username_value = tk.StringVar()
        username_entry = ttk.Entry(frame, textvariable=username_value, width=30)
        username_entry.pack(padx=10, pady=10)

        password_label = ttk.Label(frame, text="Password", font=("Open Sans", 12))
        password_label.pack(padx=10, pady=5)

        password_value = tk.StringVar()
        password_entry = ttk.Entry(frame, textvariable=password_value, width=30, show="*")
        password_entry.pack(padx=10, pady=10)

        button = ttk.Button(frame, text="Sign In",
                            command=lambda: self.login(username_value.get(), password_value.get()))
        button.pack(padx=10, pady=10)

        register_button = ttk.Button(frame, text="Create an Account", command=lambda: self.register_page())
        register_button.pack(padx=10, pady=10)

    def login(self, username, password):
        """Handles the login logic"""
        if username and password:
            user = login(username, password)
            if user:
                self.current_user = user
                self.home_page(user)
            else:
                messagebox.showerror("Invalid Input", "Wrong username and/or password")
        else:
            messagebox.showerror("Invalid Input", "Empty Fields")

    def register_page(self):
        """Register page of the application. Displays the registration form."""
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = ttk.Frame(self.root)
        frame.pack(pady=100)

        label = ttk.Label(frame, text="Register", font=("Open Sans", 24, "bold"))
        label.pack(pady=20)

        username_label = ttk.Label(frame, text="Username", font=("Open Sans", 12))
        username_label.pack(padx=10, pady=5)

        username_value = tk.StringVar()
        username_entry = ttk.Entry(frame, textvariable=username_value, width=30)
        username_entry.pack(padx=10, pady=10)

        password_label = ttk.Label(frame, text="Password", font=("Open Sans", 12))
        password_label.pack(padx=10, pady=5)

        password_value = tk.StringVar()
        password_entry = ttk.Entry(frame, textvariable=password_value, width=30, show="*")
        password_entry.pack(padx=10, pady=10)

        confirm_password_label = ttk.Label(frame, text="Confirm Password", font=("Open Sans", 12))
        confirm_password_label.pack(padx=10, pady=5)

        confirm_password_value = tk.StringVar()
        confirm_password_entry = ttk.Entry(frame, textvariable=confirm_password_value, width=30, show="*")
        confirm_password_entry.pack(padx=10, pady=10)

        button = ttk.Button(frame, text="Register", command=lambda: self.register_user(username_value.get(), password_value.get(), confirm_password_value.get()))
        button.pack(padx=10, pady=10)

        back_to_login_button = ttk.Button(frame, text="Back to Login", command=self.login_page)
        back_to_login_button.pack(padx=10, pady=10)

    def register_user(self, username, password, confirm_password):
        """Handles the registration logic"""
        if username and password:
            if password != confirm_password:
                messagebox.showerror("Invalid Input", "Passwords do not match")
            else:
                user = add_user(username, password)
                if user:
                    messagebox.showinfo("Success", "Registration successful!")
                    self.login_page()
                else:
                    messagebox.showerror("Invalid Input", "Username already exists")
        else:
            messagebox.showerror("Invalid Input", "Empty Fields")

    def home_page(self, user):
        """Displays the home page"""
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = ttk.Frame(self.root)
        frame.pack(pady=50)

        welcome_label = ttk.Label(frame, text=f"Welcome, {user.username}!", font=("Open Sans", 24, "bold"))
        welcome_label.pack(pady=20)

        task_button = ttk.Button(frame, text="Create Task", command=lambda: self.add_task_page())
        task_button.pack(pady=10)

        view_tasks_button = ttk.Button(frame, text="View Tasks", command=lambda: self.view_user_tasks())
        view_tasks_button.pack(pady=10)

        logout_button = ttk.Button(frame, text="Log Out", command=lambda: self.logout())
        logout_button.pack(pady=10)

        # Plotting completed tasks by day of the week
        self.plot_tasks(user)

    def view_user_tasks(self):
        """Displays the user's tasks in a Treeview and allows for task deletion and filtering"""
        self.filtered_status = "All"
        self.filtered_priority = "All"

        for widget in self.root.winfo_children():
            widget.destroy()

        frame = ttk.Frame(self.root)
        frame.pack(pady=50)

        # Filter options by completion status and priority
        filter_frame = ttk.Frame(frame)
        filter_frame.pack(pady=10)

        # Completion Status Filter
        completion_label = ttk.Label(filter_frame, text="Completion Status")
        completion_label.grid(row=0, column=0, padx=5)

        completion_status = ttk.Combobox(filter_frame, values=["All", "Completed", "Pending"], state="readonly")
        completion_status.set("All")  # Default value
        completion_status.grid(row=0, column=1, padx=5)

        # Priority Filter
        priority_label = ttk.Label(filter_frame, text="Priority")
        priority_label.grid(row=0, column=2, padx=5)

        priority_filter = ttk.Combobox(filter_frame, values=["All", "LOW", "MEDIUM", "HIGH"], state="readonly")
        priority_filter.set("All")  # Default value
        priority_filter.grid(row=0, column=3, padx=5)

        # Apply Filter Button
        filter_button = ttk.Button(filter_frame, text="Apply Filters", command=lambda: self.apply_filters(completion_status.get(), priority_filter.get(), frame))
        filter_button.grid(row=0, column=4, padx=5)

        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=20)

        back_button = ttk.Button(button_frame, text="Back to Home", command=lambda: self.home_page(self.current_user))
        back_button.pack(side=tk.LEFT, padx=10)

        update_button = ttk.Button(button_frame, text="Update Status", command=self.update_task_status)
        update_button.pack(side=tk.LEFT, padx=10)

        delete_button = ttk.Button(button_frame, text="Delete Task", command=self.delete_task)
        delete_button.pack(side=tk.LEFT, padx=10)

        self.display_tasks(frame)

    def apply_filters(self, completion_status, priority, frame):
        """Apply filters and update the task list based on completion status and priority"""
        # Store the filter values in the class variables
        self.filtered_status = completion_status
        self.filtered_priority = priority

        # Refresh the task list with applied filters
        self.display_tasks(frame)

    def display_tasks(self, frame):
        """Display the tasks filtered by completion status and priority"""
        columns = ("ID", "Description", "Due Date", "Priority", "Status")

        if self.tree:
            self.tree.destroy()

        self.tree = ttk.Treeview(frame, columns=columns, show="headings")
        self.tree.pack(padx=10, pady=10)

        # Set the column headings
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)

        # Get tasks based on filters
        tasks = self.filter_tasks()

        # If there are no tasks, show a message
        if not tasks:
            messagebox.showinfo("No Tasks", "No tasks match the filters or there are no tasks found in the database.")

        # Insert tasks into the Treeview
        for task in tasks:
            self.tree.insert("", tk.END, values=(task.id, task.description, task.date, task.priority, task.status))

    def filter_tasks(self):
        """Return filtered tasks based on the selected completion status and priority"""
        tasks = get_tasks_user_id(self.current_user.id)

        # Filter tasks based on the selected completion status
        if self.filtered_status != "All":
            tasks = [task for task in tasks if task.status == self.filtered_status]

        # Filter tasks based on the selected priority
        if self.filtered_priority != "All":
            tasks = [task for task in tasks if task.priority == self.filtered_priority]

        return tasks

    def delete_task(self):
        """Delete the selected task from the database"""
        selected_item = self.tree.selection()

        if selected_item:
            task_id = self.tree.item(selected_item)["values"][0]
            self.delete_task_from_db(task_id)
            self.view_user_tasks()
        else:
            messagebox.showerror("Error", "Please select a task to delete.")

    def delete_task_from_db(self, task_id):
        """Use task_id to delete the task from the database"""
        task = session.query(Task).filter_by(id=task_id).first()
        if task:
            session.delete(task)
            session.commit()

    def update_task_status(self):
        """Update the status of a selected task and set the completed date"""
        selected_item = self.tree.selection()

        if selected_item:
            # Get the task ID from the selected row
            task_id = self.tree.item(selected_item)["values"][0]

            # Fetch the task from the database using its ID
            task = get_task_id(task_id)

            if task:
                # Toggle the task status between "completed" and "pending"
                new_status = "Completed" if task.status == "Pending" else "Pending"

                # Set the completed date if the task is being marked as completed
                completed_date = datetime.now().date() if new_status == "Completed" else None

                # Update the task status and completed date in the database
                update_task(task_id, task.description, task.date, task.category, task.priority, new_status,
                            completed_date)

                # Refresh the task list
                self.view_user_tasks()
            else:
                messagebox.showerror("Error", "Task not found.")
        else:
            messagebox.showerror("Error", "Please select a task to update.")

    def plot_tasks(self, user):
        """Plot the number of tasks completed for each day of the week and circular progress chart using Matplotlib"""
        task_day_counts = self.get_task_count_by_day(user.id, status="Completed")

        days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        task_count = [task_day_counts.get(day, 0) for day in days_of_week]

        # Bar chart
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.bar(days_of_week, task_count, color='#87ae73')
        ax.set_title("Tasks Completed This Week", fontsize=14)
        ax.set_xlabel("Day of Week", fontsize=12)
        ax.set_ylabel("Tasks Completed", fontsize=12)

        # Set lowest y to 0 and ticks to increment by 1
        ax.set_ylim(bottom=0)
        ax.set_yticks(range(0, max(task_count) + 1, 1))

        ax.grid(True, axis='y', linestyle='--', alpha=0.7)

        total_tasks = len(get_tasks_user_id(user.id))  # Total tasks for the user
        completed_tasks = sum(task_count)  # Total completed tasks
        completion_percentage = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0

        # Create a circular progress chart
        fig2, ax2 = plt.subplots(figsize=(7, 7))
        wedges, _, _ = ax2.pie([completion_percentage, 100 - completion_percentage],
                               labels=["Completed", "Remaining"],
                               autopct='%1.1f%%', startangle=90, colors=["#87ae73", "#899499"],
                               wedgeprops=dict(width=0.3))
        ax2.set_title("Task Completion", fontsize=14)

        # Place both charts side by side
        canvas = FigureCanvasTkAgg(fig, master=self.root)
        canvas.get_tk_widget().pack(side=tk.LEFT, padx=20)

        canvas2 = FigureCanvasTkAgg(fig2, master=self.root)
        canvas2.get_tk_widget().pack(side=tk.LEFT)

        canvas.draw()
        canvas2.draw()

    def get_task_count_by_day(self, user_id, status="Completed"):
        """Returns a dictionary with the count of completed tasks for each day of the week based on completed_date"""
        tasks = get_tasks_user_id(user_id)

        days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        task_day_counts = Counter()

        for task in tasks:
            if task.status == status and task.completed_date:
                completed = task.completed_date

                # Ensure it's a date object (not datetime)
                if isinstance(completed, datetime):
                    completed = completed.date()

                day_index = completed.weekday()
                day_name = days_of_week[day_index]
                task_day_counts[day_name] += 1

        return task_day_counts

    def add_task_page(self):
        """Displays the add task page with a Scrollable Frame"""
        for widget in self.root.winfo_children():
            widget.destroy()

        # Create a canvas widget for scrolling
        canvas = tk.Canvas(self.root)
        canvas.pack(side="left", fill="both", expand=True)

        # Create a frame inside the canvas
        task_frame = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=task_frame, anchor="nw")

        # Configure the frame to update the scrollable region dynamically
        task_frame.bind(
            "<Configure>",
            lambda event: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        back_button = ttk.Button(task_frame, text="Back to Home", command=lambda: self.home_page(self.current_user))
        back_button.place(x=10, y=10)

        # Center the "Add New Task" title in the application
        label = ttk.Label(task_frame, text="Create New Task", font=("Open Sans", 24, "bold"))
        label.grid(row=0, column=0, columnspan=3, pady=20, padx=10)

        # Description Field
        description_field = ttk.Label(task_frame, text="Description")
        description_field.grid(row=1, column=0, pady=5, padx=10, sticky="e")
        description_value = tk.StringVar()
        description_entry = ttk.Entry(task_frame, textvariable=description_value, width=30)
        description_entry.grid(row=1, column=1, pady=5, padx=10)

        # Due Date Calendar
        date_label = ttk.Label(task_frame, text="Due Date (Pick a date)")
        date_label.grid(row=2, column=0, pady=5, padx=10, sticky="e")
        self.calendar = Calendar(task_frame, selectmode="day", date_pattern="yyyy-mm-dd")
        self.calendar.grid(row=2, column=1, pady=5, padx=10)

        # Category Field
        category_field = ttk.Label(task_frame, text="Category")
        category_field.grid(row=3, column=0, pady=5, padx=10, sticky="e")
        category_value = tk.StringVar()
        category_entry = ttk.Entry(task_frame, textvariable=category_value, width=30)
        category_entry.grid(row=3, column=1, pady=5, padx=10)

        # Priority field with combobox options "LOW", "MEDIUM", "HIGH"
        priority_field = ttk.Label(task_frame, text="Priority")
        priority_field.grid(row=4, column=0, pady=5, padx=10, sticky="e")
        priority_value = StringVar()
        priority_combobox = ttk.Combobox(task_frame, textvariable=priority_value, values=["LOW", "MEDIUM", "HIGH"], width=30)
        priority_combobox.grid(row=4, column=1, pady=5, padx=10)

        status_field = ttk.Label(task_frame, text="Status")
        status_field.grid(row=5, column=0, pady=5, padx=10, sticky="e")
        status_value = tk.BooleanVar()
        status_checkbox = ttk.Checkbutton(task_frame, text="Completed", variable=status_value)
        status_checkbox.grid(row=5, column=1, pady=5, padx=10)

        button = ttk.Button(task_frame, text="Add Task", command=lambda: self.add_task(description_value.get(), category_value.get(), priority_value.get(), status_value.get()))
        button.grid(row=6, column=0, columnspan=3, pady=20)

        for i in range(6):
            task_frame.grid_columnconfigure(i, weight=1, uniform="equal")
        task_frame.grid_rowconfigure(6, weight=1, uniform="equal")

    def add_task(self, description, category, priority, status):
        """Handles adding a task"""
        selected_date = self.calendar.get_date()
        if all([description, category, priority, status is not None]):
            try:
                date = datetime.strptime(selected_date, "%Y-%m-%d").date()
            except ValueError:
                messagebox.showerror("Invalid Input", "Date format is incorrect.")
            add_task(self.current_user.id, description, date, category, priority, "Completed" if status else "Pending")
            self.home_page(self.current_user)
        else:
            messagebox.showerror("Invalid Input", "Empty Fields")

    def logout(self):
        """Logs out the user and returns to the login page"""
        self.current_user = None
        for widget in self.root.winfo_children():
            widget.destroy()
        self.login_page()


if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerGUI(root)
    root.mainloop()