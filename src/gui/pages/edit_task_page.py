import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from datetime import datetime
from ..widgets.styled_frame import StyledFrame

# Edit task page
class EditTaskPage(StyledFrame):
    def __init__(self, parent, current_user, on_back, db, current_task):
        super().__init__(parent)
        self.current_user = current_user
        self.db = db
        self.on_back = on_back
        self.parent = parent
        self.current_task = current_task
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
        ttk.Label(main_frame, text="Edit Task",
                 font=("Open Sans", 24, "bold")).pack(pady=20)

        # Form frame
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(expand=True, fill=tk.BOTH)

        # Description
        ttk.Label(form_frame, text="Description:").pack(anchor="w", pady=(10,0))
        self.description_var = tk.StringVar(value = self.current_task.description)
        ttk.Entry(form_frame, textvariable=self.description_var,
                 width=50).pack(fill=tk.X, pady=(5,10))

        # Due Date
        ttk.Label(form_frame, text="Due Date:").pack(anchor="w", pady=(10,0))
        self.calendar = Calendar(form_frame, selectmode="day",date_pattern="yyyy-mm-dd", showweeknumbers=False)
        self.calendar.selection_set(self.current_task.date)
        self.calendar.pack(pady=(5,10))

        # Priority
        ttk.Label(form_frame, text="Priority:").pack(anchor="w", pady=(10,0))
        self.priority_var = tk.StringVar()
        priority_combo = ttk.Combobox(form_frame, textvariable=self.priority_var,
                                    values=["LOW", "MEDIUM", "HIGH"],
                                    state="readonly")
        priority_combo.pack(fill=tk.X, pady=(5,10))
        priority_combo.set(self.current_task.priority)  # Default value

        # Status
        ttk.Label(form_frame, text="Status:").pack(anchor="w", pady=(10,0))
        self.status_var = tk.StringVar()
        status_combo = ttk.Combobox(form_frame, textvariable=self.status_var,values=["Pending", "Completed"],state="readonly")
        status_combo.pack(fill=tk.X, pady=(5,10))
        status_combo.set(self.current_task.status)  # Default value

        # Add Task button
        ttk.Button(form_frame, text="Edit Task",
                  command=self.edit_task).pack(pady=20)

    # Re-route
    def go_back(self):
        self.destroy()  # Destroy current page
        self.on_back()

    def edit_task(self):
        """Handle task creation"""
        description = self.description_var.get()
        date = self.calendar.get_date()
        priority = self.priority_var.get()
        status = self.status_var.get()

        if all([description, date, priority, status]):
            try:
                completed_date = datetime.now().date() if status == "Completed" else None
                date_obj = datetime.strptime(date, "%Y-%m-%d").date()
                self.db.update_task(
                    task_id=self.current_task.id,
                    description=description,
                    date=date_obj,
                    priority=priority,
                    status=status,
                    completed_date= completed_date
                )
                self.go_back()
            except ValueError:
                messagebox.showerror("Error", "Invalid date format")
        else:
            messagebox.showerror("Error", "Please fill all fields")