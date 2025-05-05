import tkinter as tk
from tkinter import ttk, messagebox
from src.gui.widgets.styled_frame import StyledFrame

class LoginPage(StyledFrame):
    def __init__(self, parent, on_login_success, db):
        super().__init__(parent)
        self.db = db
        self.on_login_success = on_login_success
        self.setup_ui()

    def setup_ui(self):
        """Setup login page UI"""
        frame = ttk.Frame(self)
        frame.pack(pady=100)

        # Title
        ttk.Label(frame, text="Taskify", font=("Open Sans", 24, "bold")).pack(pady=20)

        # Username
        ttk.Label(frame, text="Username", font=("Open Sans", 12)).pack(pady=5)
        self.username_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.username_var, width=30).pack(pady=10)

        # Password
        ttk.Label(frame, text="Password", font=("Open Sans", 12)).pack(pady=5)
        self.password_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.password_var, width=30, show="*").pack(pady=10)

        # Buttons
        ttk.Button(frame, text="Sign In", command=self.handle_login).pack(pady=10)
        ttk.Button(frame, text="Create an Account",
                   command=self.show_register_page).pack(pady=10)

    def handle_login(self):
        """Handle login attempt"""
        username = self.username_var.get()
        password = self.password_var.get()

        if username and password:
            user = self.db.login(username, password)
            if user:
                self.on_login_success(user)
            else:
                messagebox.showerror("Error", "Invalid credentials")
        else:
            messagebox.showerror("Error", "Please fill all fields")

    def show_register_page(self):
        """Switch to registration page"""
        from .register_page import RegisterPage
        for widget in self.master.winfo_children():
            widget.destroy()
        RegisterPage(self.master, self.db)
