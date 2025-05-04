import tkinter as tk
from src.gui.pages.login_page import LoginPage
from src.gui.pages.home_page import HomePage
from src.database.db_manager import DatabaseManager

class TaskManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Taskify - Task Manager")
        self.root.geometry("1000x800")
        self.root.config(bg="white")
        self.current_user = None
        self.db = DatabaseManager()
        self.show_login_page()

    def show_login_page(self):
        """Switch to login page"""
        for widget in self.root.winfo_children():
            widget.destroy()
        LoginPage(self.root, self.on_login_success, self.db)

    def show_home_page(self):
        """Switch to home page"""
        for widget in self.root.winfo_children():
            widget.destroy()
        HomePage(self.root, self.current_user, self.show_login_page, self.db)

    def on_login_success(self, user):
        """Handle successful login"""
        self.current_user = user
        self.show_home_page()
