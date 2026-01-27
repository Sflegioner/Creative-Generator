
import tkinter as tk
from gui.main_window import MainWindow
from core.Folder_manager import FolderManager


if  __name__ == "__main__":
    root = tk.Tk()
    f = FolderManager()

    m = MainWindow(root,f,)
    root.mainloop()
    pass    