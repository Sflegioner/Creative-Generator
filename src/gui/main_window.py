from tkinter import *
from tkinter import ttk
from .components.Card import Card
from .components.Button import Button
from core.Folder_manager import FolderManager

class MainWindow():

    def __init__(self,root:Tk, folder_manager:FolderManager):
        self.root = root
        self.root.configure(bg="#262626")
        self.style = ttk.Style(self.root)
        self.style.configure('.',
                                background="#262626",
                                foreground="#e0e0ff",
                                font=('Segoe UI', 11))
        self.root.resizable(True, True)
        
        self.folder_manager = folder_manager

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
            size_h = 1080 - 2 * margin 

            card1 = Card(
                root=self.root,
                pos_x=(self.screen_w - size_w) // 2,
                pos_y=(1080 - size_h) // 2,
                size=(size_w, size_h),
                layer=5,
                text="Work Space",
                bg_color="#3B3B3B" 
            )

            card2 = Card(
                root=self.root,
                pos_x=30,
                pos_y=70,
                size=(200, 600),
                layer=6,
                text="Folder Space",
                bg_color="#3B3B3B" 
            )
            
            card3 = Card(
                root=self.root,
                pos_x=300,
                pos_y=70,
                size=(500, 600),
                layer=6,
                text="Before",
                bg_color="#3B3B3B" 
            )
            
            card4 = Card(
                root=self.root,
                pos_x=850,
                pos_y=70,
                size=(500, 600),
                layer=6,
                text="After",
                bg_color="#3B3B3B" 
            )
            
            tool_card = Card(
                root=self.root,
                pos_x=30,
                pos_y=700,
                size=(1450, 80),
                layer=6,
                text="Tools",
                bg_color="#3B3B3B" 
            )
            #======================================================
            choose_bg = Button(
                tool_card.card_canvas,
                pos_x=40,
                pos_y=45,
                size=(120,25),
                layer=8,
                text="Add background",
                bg_color="#D6D6D6",
                icon_path=None,
                active=False
            )
            add_card_image = Button(
                tool_card.card_canvas,
                pos_x=200,
                pos_y=45,
                size=(120,25),
                layer=8,
                text="Add card",
                bg_color="#D6D6D6",
                icon_path=None,
                active=False
            )
            add_selebrity = Button(
                tool_card.card_canvas,
                pos_x=360,
                pos_y=45,
                size=(120,25),
                layer=8,
                text="Add celebrity",
                bg_color="#D6D6D6",
                icon_path=None,
                active=False
            )
            add_object = Button(
                tool_card.card_canvas,
                pos_x=520,
                pos_y=45,
                size=(120,25),
                layer=8,
                text="Add object",
                bg_color="#D6D6D6",
                icon_path=None,
                active=False
            )
            add_text_fild = Button(
                tool_card.card_canvas,
                pos_x=680,
                pos_y=45,
                size=(120,25),
                layer=8,
                text="Add text field",
                bg_color="#D6D6D6",
                icon_path=None,
                active=False
            )
            insert_all = Button(
                tool_card.card_canvas,
                pos_x=840,
                pos_y=45,
                size=(120,25),
                layer=8,
                text="Insert all",
                bg_color="#947432",
                icon_path=None,
                active=False
            )
            save_all = Button(
                tool_card.card_canvas,
                pos_x=1000,
                pos_y=45,
                size=(120,25),
                layer=8,
                text="Save all",
                bg_color="#286818",
                icon_path=None,
                active=False
            )
            
            #=====================ToolsButton=================================
            b1 = Button(
                card2.card_canvas,
                pos_x=25,
                pos_y=100,
                size=(120,40),
                layer=8,
                text="Backgounds",
                bg_color="#1E1E1E",
                callback_function=lambda: self.on_folder_button_click(b1, self.folder_manager.take_background_folder),
                icon_path=None,
                active=False
            )
            b2 = Button(
                card2.card_canvas,
                pos_x=25,
                pos_y=200,
                size=(120,40),
                layer=8,
                text="Card balance",
                bg_color="#1E1E1E",
                callback_function=lambda: self.on_folder_button_click(b2, self.folder_manager.take_items_folder),  # Assuming "Card balance" is for items
                icon_path=None,
                active=False
            )
            b3 = Button(
                card2.card_canvas,
                pos_x=25,
                pos_y=300,
                size=(120,40),
                layer=8,
                text="Selebrity",
                bg_color="#1E1E1E",
                callback_function=lambda: self.on_folder_button_click(b3, self.folder_manager.take_celebrities_folder),
                icon_path=None,
                active=False
            )          
            b4 = Button(
                card2.card_canvas,
                pos_x=25,
                pos_y=400,
                size=(120,40),
                layer=8,
                text="Objects",
                bg_color="#1E1E1E",
                callback_function=lambda: self.on_folder_button_click(b4, self.folder_manager.take_object_folder),
                icon_path=None,
                active=False
            )
            b5 = Button(
                card2.card_canvas,
                pos_x=25,
                pos_y=500,
                size=(120,40),
                layer=8,
                text="File of texts",
                bg_color="#1E1E1E",
                callback_function=lambda: self.on_folder_button_click(b5, self.folder_manager.take_text_file),
                icon_path=None,
                active=False
            )
            
            self.buttons = [b1, b2, b3, b4, b5] 
    
    def on_folder_button_click(self, button: Button, func):
        #  button manages its own active state independently
        func(button)