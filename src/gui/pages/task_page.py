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
        self.parent = parent
        self.pack(fill=tk.BOTH, expand=True)
        self.setup_ui()

    def setup_ui(self):
        """Setup task creation UI"""
        # Create main frame
        main_frame = ttk.Frame(self)
        main_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

        # Back button
        ttk.Button(main_frame, text="Back",
                  command=self.go_back).pack(anchor="w", pady=10)

        # Title
        ttk.Label(main_frame, text="Create New Task",
                 font=("Open Sans", 24, "bold")).pack(pady=20)

        # Form frame
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(expand=True, fill=tk.BOTH)

        # Description
        ttk.Label(form_frame, text="Description:").pack(anchor="w", pady=(10,0))
        self.description_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.description_var,
                 width=50).pack(fill=tk.X, pady=(5,10))

        # Due Date
        ttk.Label(form_frame, text="Due Date:").pack(anchor="w", pady=(10,0))
        self.calendar = Calendar(form_frame, selectmode="day",date_pattern="yyyy-mm-dd", showweeknumbers=False)
        self.calendar.pack(pady=(5,10))

        # Priority
        ttk.Label(form_frame, text="Priority:").pack(anchor="w", pady=(10,0))
        self.priority_var = tk.StringVar()
        priority_combo = ttk.Combobox(form_frame, textvariable=self.priority_var,
                                    values=["LOW", "MEDIUM", "HIGH"],
                                    state="readonly")
        priority_combo.pack(fill=tk.X, pady=(5,10))
        priority_combo.set("MEDIUM")  # Default value

        # Add Task button
        ttk.Button(form_frame, text="Add Task",
                  command=self.add_task).pack(pady=20)

    def go_back(self):
        """Safe way to go back"""
        self.destroy()  # Destroy current page
        self.on_back()  # Call the callback to show home page

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
                    priority=priority,
                    status="Pending"
                )
                self.go_back()
            except ValueError:
                messagebox.showerror("Error", "Invalid date format")
        else:
            messagebox.showerror("Error", "Please fill all fields")