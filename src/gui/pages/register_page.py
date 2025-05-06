import tkinter as tk
from tkinter import ttk, messagebox
from ..widgets.styled_frame import StyledFrame

# Register page, handles user registration and adds user to the database.
class RegisterPage(StyledFrame):
    def __init__(self, parent, db, on_login_success):
        super().__init__(parent)
        self.db = db
        self.on_login_success = on_login_success  # Pass it to RegisterPage
        self.setup_ui()

    def setup_ui(self):
        frame = ttk.Frame(self)
        frame.pack(pady=100)

        ttk.Label(frame, text="Register", font=("Open Sans", 24, "bold")).pack(pady=20)

        ttk.Label(frame, text="Username", font=("Open Sans", 12)).pack(pady=5)
        self.username_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.username_var, width=30).pack(pady=10)

        ttk.Label(frame, text="Password", font=("Open Sans", 12)).pack(pady=5)
        self.password_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.password_var, width=30, show="*").pack(pady=10)

        ttk.Label(frame, text="Confirm Password", font=("Open Sans", 12)).pack(pady=5)
        self.confirm_password_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.confirm_password_var, width=30, show="*").pack(pady=10)

        ttk.Button(frame, text="Register", command=self.handle_register).pack(pady=10)
        ttk.Button(frame, text="Back to Login", command=self.back_to_login).pack(pady=10)

    # Checks username does not already exist and that the passwords match before adding to database.
    def handle_register(self):
        username = self.username_var.get()
        password = self.password_var.get()
        confirm_password = self.confirm_password_var.get()

        if username and password:
            if password != confirm_password:
                messagebox.showerror("Error", "Passwords do not match")
            else:
                user = self.db.add_user(username, password)
                if user:
                    messagebox.showinfo("Success", "Registration successful!")
                    self.back_to_login()
                else:
                    messagebox.showerror("Error", "Username already exists")
        else:
            messagebox.showerror("Error", "Please fill all fields")

    # Switch back to the login page
    def back_to_login(self):
        """Switch back to the login page"""
        from .login_page import LoginPage
        for widget in self.master.winfo_children():
            widget.destroy()
        LoginPage(self.master, self.on_login_success, self.db)