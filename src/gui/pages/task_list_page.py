import tkinter as tk
from tkinter import ttk, messagebox
from ..widgets.styled_frame import StyledFrame
from datetime import datetime

# Task list page that allows user to update task status, delete task, create new task, sort tasks, and filter tasks.
class TaskListPage(StyledFrame):
    def __init__(self, parent, user, on_back, db):
        super().__init__(parent)
        self.user = user
        self.db = db
        self.on_back = on_back
        self.parent = parent
        self.filtered_status = "All"
        self.filtered_priority = "All"
        self.sort_column = None  # For keeping track of the current sorting column
        self.sort_reverse = False  # For toggling sorting order
        self.pack(fill=tk.BOTH, expand=True)
        self.setup_ui()

    def setup_ui(self):
        main_frame = ttk.Frame(self)
        main_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

        # Title
        ttk.Label(main_frame, text="Your Tasks",
                 font=("Open Sans", 24, "bold")).pack(pady=20)

        # Filter frame
        filter_frame = ttk.Frame(main_frame)
        filter_frame.pack(fill=tk.X, pady=10)

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

        # Apply filters button
        ttk.Button(filter_frame, text="Apply Filters",
                  command=self.apply_filters).grid(row=0, column=4, padx=5)

        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Back",
                  command=self.go_back).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Update Status",
                  command=self.update_task_status).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Delete Task",
                  command=self.delete_task).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Edit Task",
                   command=self.edit_task).pack(side=tk.LEFT, padx=5)

        # Create task tree
        self.create_task_tree(main_frame)
        self.load_tasks()

    # Create task tree and load tasks from database
    # This function is called when the page is first loaded or when the filters are applied.
    # It creates a task tree widget and loads tasks from the database based on the current filters.
    # The tree is sorted by the current sorting column and order.
    # If no sorting column is set, the tasks are sorted by ID in ascending order.
    # If the sorting column is set, the tasks are sorted by that column in the current sorting order.
    # If the sorting order is toggled, the tasks are sorted in the opposite order.
    # The sorting column and order are stored in the class attributes for future use.
    def create_task_tree(self, parent):
        columns = ("ID", "Description", "Due Date", "Priority", "Status")
        self.tree = ttk.Treeview(parent, columns=columns, show="headings")

        # Make column headers clickable to sort
        for col in columns:
            self.tree.heading(col, text=col, command=lambda c=col: self.sort_by_column(c))
            self.tree.column(col, width=150)

        self.tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    def sort_by_column(self, column):
        column_mapping = {
            "ID": "id",
            "Description": "description",
            "Due Date": "date",
            "Priority": "priority",
            "Status": "status"
        }

        task_column = column_mapping.get(column)
        if not task_column:
            print(f"[ERROR] No matching Task attribute found for column: {column}")
            return

        if self.sort_column == task_column:
            self.sort_reverse = not self.sort_reverse
        else:
            self.sort_column = task_column
            self.sort_reverse = False

        tasks = self.get_filtered_tasks()

        if column == "Priority":
            priority_order = {"LOW": 0, "MEDIUM": 1, "HIGH": 2}
            tasks.sort(key=lambda t: priority_order.get(t.priority, 0), reverse=self.sort_reverse)
        elif column == "Status":
            status_order = {"Pending": 0, "Completed": 1}
            tasks.sort(key=lambda t: status_order.get(t.status, 0), reverse=self.sort_reverse)
        else:
            tasks.sort(key=lambda t: getattr(t, task_column), reverse=self.sort_reverse)

        self.tree.delete(*self.tree.get_children())
        for task in tasks:
            self.tree.insert("", tk.END, values=(
                task.id, task.description, task.date, task.priority, task.status
            ))

    # Load tasks from database based on the current filters
    # This function is called when the filters are applied.
    # It retrieves tasks from the database based on the current filters and sorts them.
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

    # Get filtered tasks from database based on the current filters
    # This function is called when the page is first loaded or when the filters are applied.
    # It retrieves tasks from the database based on the current filters and returns them.
    # The filters are applied based on the current status and priority values.
    # If no filters are applied, all tasks are returned.
    # If only the status filter is applied, only tasks with the specified status are returned.
    # If only the priority filter is applied, only tasks with the specified priority are returned.
    # If both filters are applied, tasks with the specified status and priority are returned.
    def get_filtered_tasks(self):
        tasks = self.db.get_tasks_by_user_id(self.user.id)

        if self.filtered_status != "All":
            tasks = [t for t in tasks if t.status == self.filtered_status]
        if self.filtered_priority != "All":
            tasks = [t for t in tasks if t.priority == self.filtered_priority]

        return tasks

    # Apply filters to the task list
    # This function is called when the Apply Filters button is clicked.
    # It sets the current status and priority filters to the values selected in the comboboxes.
    # It then calls the load_tasks function to update the task list with the new filters.
    def apply_filters(self):
        self.filtered_status = self.status_var.get()
        self.filtered_priority = self.priority_var.get()
        self.load_tasks()

    # Update task status
    # This function is called when the Update Status button is clicked.
    # It retrieves the selected task from the tree and updates its status based on the current status.
    # If the task is currently Pending, it is set to Completed.
    # If the task is currently Completed, it is set to Pending.
    # The completed_date attribute is set to the current date if the task is set to Completed.
    # The updated task is then saved to the database and the task list is updated.
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
                priority=task.priority,
                status=new_status,
                completed_date=completed_date
            )
            self.load_tasks()

    # Delete task
    # This function is called when the Delete Task button is clicked.
    # It retrieves the selected task from the tree and deletes it from the database.
    # The task list is then updated.
    def delete_task(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a task")
            return

        if messagebox.askyesno("Confirm", "Are you sure you want to delete this task?"):
            task_id = self.tree.item(selected[0])["values"][0]
            self.db.delete_task(task_id)
            self.load_tasks()

    # Edit task
    # This function is called when the Edit Task button is clicked.
    # It retrieves the selected task from the tree and opens an edit task page for the task.
    # The edit task page is destroyed when it is closed.
    # The task list is then updated.
    # This function is called when the Edit Task button is clicked.
    # It retrieves the selected task from the tree and opens an edit task page for the task.
    # The edit task page is destroyed when it is closed.
    def edit_task(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a task")
            return
        task_id = self.tree.item(selected[0])["values"][0]
        task = self.db.get_task_by_id(task_id)
        if task:
            from .edit_task_page import EditTaskPage
            self.destroy()  # Destroy current page
            EditTaskPage(self.parent, self.user, self.go_back_task_page, self.db, task)
            # self.load_tasks()

    # Go back to previous page
    def go_back(self):
        self.destroy()
        self.on_back()

    # Go back to tasklist page
    def go_back_task_page(self):
        self.destroy()
        TaskListPage(self.parent, self.user, self.go_back, self.db)