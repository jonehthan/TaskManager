import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


class TaskList(ttk.Frame):
    def __init__(self, parent, user, on_back, db):
        super().__init__(parent)
        self.user = user
        self.db = db
        self.on_back = on_back
        self.tree = None
        self.filtered_status = "All"
        self.filtered_priority = "All"
        self.setup_ui()
        self.pack(fill=tk.BOTH, expand=True)

    def setup_ui(self):
        # Filter frame
        filter_frame = ttk.Frame(self)
        filter_frame.pack(pady=10)

        # Status filter
        ttk.Label(filter_frame, text="Status:").grid(row=0, column=0, padx=5)
        self.status_var = tk.StringVar(value="All")
        ttk.Combobox(filter_frame, textvariable=self.status_var,
                     values=["All", "Completed", "Pending"],
                     state="readonly").grid(row=0, column=1, padx=5)

        # Priority filter
        ttk.Label(filter_frame, text="Priority:").grid(row=0, column=2, padx=5)
        self.priority_var = tk.StringVar(value="All")
        ttk.Combobox(filter_frame, textvariable=self.priority_var,
                     values=["All", "LOW", "MEDIUM", "HIGH"],
                     state="readonly").grid(row=0, column=3, padx=5)

        ttk.Button(filter_frame, text="Apply Filters",
                   command=self.apply_filters).grid(row=0, column=4, padx=5)

        # Buttons frame
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Back",
                   command=self.on_back).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Update Status",
                   command=self.update_task_status).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Delete Task",
                   command=self.delete_task).pack(side=tk.LEFT, padx=5)

        # Task list
        self.create_task_tree()
        self.load_tasks()

    def create_task_tree(self):
        columns = ("ID", "Description", "Due Date", "Priority", "Status")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)

        self.tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    def load_tasks(self):
        tasks = self.get_filtered_tasks()

        self.tree.delete(*self.tree.get_children())

        for task in tasks:
            self.tree.insert("", tk.END, values=(
                task.id,
                task.description,
                task.date,
                task.priority,
                task.status
            ))

    def get_filtered_tasks(self):
        tasks = self.db.get_tasks_by_user_id(self.user.id)

        if self.filtered_status != "All":
            tasks = [t for t in tasks if t.status == self.filtered_status]
        if self.filtered_priority != "All":
            tasks = [t for t in tasks if t.priority == self.filtered_priority]

        return tasks

    def apply_filters(self):
        self.filtered_status = self.status_var.get()
        self.filtered_priority = self.priority_var.get()
        self.load_tasks()

    def update_task_status(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a task")
            return

        task_id = self.tree.item(selected[0])["values"][0]
        task = self.db.get_task_by_id(task_id)

        if task:
            new_status = "Completed" if task.status == "Pending" else "Pending"
            completed_date = datetime.now().date() if new_status == "Completed" else None

            self.db.update_task(
                task_id=task_id,
                description=task.description,
                date=task.date,
                category=task.category,
                priority=task.priority,
                status=new_status,
                completed_date=completed_date
            )
            self.load_tasks()

    def delete_task(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a task")
            return

        if messagebox.askyesno("Confirm", "Are you sure you want to delete this task?"):
            task_id = self.tree.item(selected[0])["values"][0]
            self.db.delete_task(task_id)
            self.load_tasks()