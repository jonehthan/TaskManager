import tkinter as tk
from src.database.db_config import init_db
from src.gui.main_window import TaskManagerGUI

def main():
    init_db()
    root = tk.Tk()
    app = TaskManagerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()