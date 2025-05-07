import tkinter as tk
from tkinter import ttk
from ..widgets.task_chart import TaskChart
from .task_list_page import TaskListPage

# Home page that contains routing back to the login, add task, and view task pages
class HomePage(ttk.Frame):
    def __init__(self, parent, user, on_logout, db):
        super().__init__(parent)
        self.user = user
        self.db = db
        self.on_logout = on_logout
        self.parent = parent
        self.pack(fill=tk.BOTH, expand=True)
        self.setup_ui()

    def setup_ui(self):
        # Clear existing widgets
        for widget in self.winfo_children():
            widget.destroy()

        frame = ttk.Frame(self)
        frame.pack(pady=50)

        # Welcome message
        welcome_label = ttk.Label(frame,
                                text=f"Welcome, {self.user.username}!",
                                font=("Open Sans", 24, "bold"))
        welcome_label.pack(pady=20)

        # Buttons
        buttons_frame = ttk.Frame(frame)
        buttons_frame.pack(pady=10)

        ttk.Button(buttons_frame, text="Create Task",
                  command=self.show_add_task).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="View Tasks",
                  command=self.show_task_list).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Log Out",
                  command=self.on_logout).pack(side=tk.LEFT, padx=5)

        # Charts
        self.display_charts()

    # Show charts if the user has any tasks
    def display_charts(self):
        tasks = self.db.get_tasks_by_user_id(self.user.id)
        if tasks:
            chart = TaskChart(self, tasks)
            chart.plot_completion_charts()

    # Page rerouting functions
    def show_add_task(self):
        from .task_page import TaskPage
        self.destroy()  # Destroy current page
        TaskPage(self.parent, self.user, self.return_to_home, self.db)

    def show_task_list(self):
        self.destroy()  # Destroy current page
        TaskListPage(self.parent, self.user, self.return_to_home, self.db)

    def return_to_home(self):
        """Return to home page"""
        self.destroy()
        HomePage(self.parent, self.user, self.on_logout, self.db)