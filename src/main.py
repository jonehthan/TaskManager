import tkinter as tk
from src.database.db_config import init_db
from src.gui.main_window import TaskManagerGUI

# Main function to run the application.
def main():
    init_db()
    root = tk.Tk()
    app = TaskManagerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()