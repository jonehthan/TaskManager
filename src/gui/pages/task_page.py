import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from datetime import datetime
from ..widgets.styled_frame import StyledFrame

class TaskPage(StyledFrame):
    def __init__(self, parent, current_user, on_back, db):
        super().__init__(parent)
        self.current_user = current_user
        self.db = db
        self.on_back = on_back
        self.setup_ui()

    def setup_ui(self):
        """Setup task creation UI"""
        # Create scrollable canvas
        canvas = tk.Canvas(self)
        canvas.pack(side="left", fill="both", expand=True)

        task_frame = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=task_frame, anchor="nw")

        # Back button
        ttk.Button(task_frame, text="Back",
                  command=self.on_back).grid(row=0, column=0, pady=10)

        # Title
        ttk.Label(task_frame, text="Create New Task",
                 font=("Open Sans", 24, "bold")).grid(row=1, column=0,
                                                    columnspan=2, pady=20)

        # Description
        ttk.Label(task_frame, text="Description").grid(row=2, column=0, pady=5)
        self.description_var = tk.StringVar()
        ttk.Entry(task_frame, textvariable=self.description_var,
                 width=30).grid(row=2, column=1, pady=5)

        # Due Date
        ttk.Label(task_frame, text="Due Date").grid(row=3, column=0, pady=5)
        self.calendar = Calendar(task_frame, selectmode="day",
                               date_pattern="yyyy-mm-dd")
        self.calendar.grid(row=3, column=1, pady=5)

        # Priority
        ttk.Label(task_frame, text="Priority").grid(row=4, column=0, pady=5)
        self.priority_var = tk.StringVar()
        ttk.Combobox(task_frame, textvariable=self.priority_var,
                    values=["LOW", "MEDIUM", "HIGH"]).grid(row=4, column=1, pady=5)

        # Add Task button
        ttk.Button(task_frame, text="Add Task",
                  command=self.add_task).grid(row=5, column=0,
                                            columnspan=2, pady=20)

    def add_task(self):
        """Handle task creation"""
        description = self.description_var.get()
        date = self.calendar.get_date()
        priority = self.priority_var.get()

        if all([description, date, priority]):
            try:
                date_obj = datetime.strptime(date, "%Y-%m-%d").date()
                self.db.add_task(
                    user_id=self.current_user.id,
                    description=description,
                    date=date_obj,
                    category="General",  # Default category
                    priority=priority,
                    status="Pending"
                )
                self.on_back()
            except ValueError:
                messagebox.showerror("Error", "Invalid date format")
        else:
            messagebox.showerror("Error", "Please fill all fields")
