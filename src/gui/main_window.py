
from tkinter import *
from tkinter import ttk
from .components.Card import Card

class MainWindow():

    def __init__(self,root:Tk):
        self.root = root
        self.root.configure(bg="#262626")
        self.style = ttk.Style(self.root)
        self.style.configure('.',
                                background="#262626",
                                foreground="#e0e0ff",
                                font=('Segoe UI', 11))
        self.root.resizable(True, True)

        self.screen_w =self.root.winfo_screenwidth()
        self.screen_h = self.root.winfo_screenheight()

        self.draw_window()
        self.draw_logo()
        self.draw_main_space()

      
    def draw_window(self):
        self.root.geometry("1920x1080")
        #self.root.maxsize(1920, 1080)
        self.root.minsize(300, 200)

        w, h = 800, 600
        x = (self.screen_w - w) // 2
        y = (self.screen_h - h) // 2
        #TODO:Change this to center window
        self.root.geometry(f"{self.screen_w}x{self.screen_h}")
        #self.root.geometry(f"{w}x{h}+{x}+{y}")

        
    def draw_logo(self):
        label = ttk.Label(self.root,text="TEMKA CREATIVE")
        label.pack(pady=0)

    def draw_main_space(self):
            margin = 25
            size_w = self.screen_w - 2 * margin
            size_h = 1080 - 2 * margin  # Assuming screen height is 1080; adjust if self.screen_h exists

            card1 = Card(
                root=self.root,
                pos_x=(self.screen_w - size_w) // 2,
                pos_y=(1080 - size_h) // 2,
                size=(size_w, size_h),
                layer=5,
                text="Work Space",
                bg_color="#3B3B3B" 
            )
            pass