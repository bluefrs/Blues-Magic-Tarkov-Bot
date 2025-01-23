from gui import App
import tkinter as tk
from config import ensure_bot_directory

if __name__ == "__main__":
    ensure_bot_directory()  # Ensure the directory exists before starting
    root = tk.Tk()
    app = App(root)
    root.mainloop()
