import tkinter as tk
from tkinter import ttk
from ..widgets.task_chart import TaskChart
from ..widgets.task_list import TaskList

class HomePage(ttk.Frame):
    def __init__(self, parent, user, on_logout, db):
        super().__init__(parent)
        self.user = user
        self.db = db
        self.on_logout = on_logout
        self.pack(fill=tk.BOTH, expand=True)
        self.setup_ui()

    def setup_ui(self):
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

    def display_charts(self):
        tasks = self.db.get_tasks_by_user_id(self.user.id)
        chart = TaskChart(self, tasks)
        chart.plot_completion_charts()

    def show_add_task(self):
        from .task_page import TaskPage
        for widget in self.master.winfo_children():
            widget.destroy()
        TaskPage(self.master, self.user, self.refresh, self.db)

    def show_task_list(self):
        TaskList(self.master, self.user, self.refresh, self.db)

    def refresh(self):
        for widget in self.master.winfo_children():
            widget.destroy()
        self.setup_ui()