from tkinter import *
from tkinter import ttk
from .components.Card import Card
from .components.Button import Button
from core.Folder_manager import FolderManager
from core.Canvas import Canvas

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
        #self.root.geometry("1920x1080")
        #self.root.maxsize(1920, 1080)
        self.root.minsize(300, 200)

        w, h = 1280, 720
        x = (self.screen_w - w) // 2
        y = (self.screen_h - h) // 2
        #TODO:Change this to center window
        #self.root.geometry(f"{self.screen_w}x{self.screen_h}")
        self.root.geometry(f"{w}x{h}+{x}+{y}")

        
    def draw_logo(self):
        label = ttk.Label(self.root,text="TEMKA CREATIVE")
        label.pack(pady=0)
        
    def add_field_to_both(self, item_type: str):
        self.before_canvas.add_item(item_type)
        self.after_canvas.add_item(item_type)

    def insert_all(self):
        self.before_canvas.insert_content(self.folder_manager)
        self.after_canvas.insert_content(self.folder_manager)

    def save_all(self):
        self.before_canvas.save_composition("before_composition.png")
        self.after_canvas.save_composition("after_composition.png")

    def draw_main_space(self):
            margin = 20
            folder_w = 200
            folder_h = 600
            folder_x = margin
            folder_y = 70

            card2 = Card(
                root=self.root,
                pos_x=folder_x,
                pos_y=folder_y,
                size=(folder_w, folder_h),
                layer=6,
                text="Folder Space",
                bg_color="#3B3B3B" 
            )
            
            gap = margin
            before_x = folder_x + folder_w + gap
            available_w = self.screen_w - before_x - margin
            canvas_h = min(600, self.screen_h - 200)
            before_w = available_w // 2 - gap // 2
            after_w = before_w
            after_x = before_x + before_w + gap
            
            card3 = Card(
                root=self.root,
                pos_x=before_x,
                pos_y=folder_y,
                size=(before_w, canvas_h),
                layer=6,
                text="Before",
                bg_color="#3B3B3B" 
            )
            
            card4 = Card(
                root=self.root,
                pos_x=after_x,
                pos_y=folder_y,
                size=(after_w, canvas_h),
                layer=6,
                text="After",
                bg_color="#3B3B3B" 
            )
            
            tool_x = margin
            tool_y = folder_y + max(folder_h, canvas_h) + margin
            tool_w = self.screen_w - 2 * margin
            tool_h = 80
            tool_card = Card(
                root=self.root,
                pos_x=tool_x,
                pos_y=tool_y,
                size=(tool_w, tool_h),
                layer=6,
                text="Tools",
                bg_color="#3B3B3B" 
            )
            #======================================================
            tool_button_w = 100
            tool_button_h = 25
            tool_button_dx = 110
            tool_button_start_x = 20
            tool_button_y = 35

            choose_bg = Button(
                tool_card.card_canvas,
                pos_x=tool_button_start_x + 0 * tool_button_dx,
                pos_y=tool_button_y,
                size=(tool_button_w, tool_button_h),
                layer=8,
                text="Add background",
                bg_color="#1E1E1E",
                icon_path=None,
                active=False
            )
            add_card_image = Button(
                tool_card.card_canvas,
                pos_x=tool_button_start_x + 1 * tool_button_dx,
                pos_y=tool_button_y,
                size=(tool_button_w, tool_button_h),
                layer=8,
                text="Add card",
                bg_color="#1E1E1E",
                icon_path=None,
                active=False
            )
            add_selebrity = Button(
                tool_card.card_canvas,
                pos_x=tool_button_start_x + 2 * tool_button_dx,
                pos_y=tool_button_y,
                size=(tool_button_w, tool_button_h),
                layer=8,
                text="Add celebrity",
                bg_color="#1E1E1E",
                icon_path=None,
                active=False
            )
            add_object = Button(
                tool_card.card_canvas,
                pos_x=tool_button_start_x + 3 * tool_button_dx,
                pos_y=tool_button_y,
                size=(tool_button_w, tool_button_h),
                layer=8,
                text="Add object",
                bg_color="#1E1E1E",
                icon_path=None,
                active=False
            )
            add_text_fild = Button(
                tool_card.card_canvas,
                pos_x=tool_button_start_x + 4 * tool_button_dx,
                pos_y=tool_button_y,
                size=(tool_button_w, tool_button_h),
                layer=8,
                text="Add text field",
                bg_color="#1E1E1E",
                icon_path=None,
                active=False
            )
            insert_all = Button(
                tool_card.card_canvas,
                pos_x=tool_button_start_x + 5 * tool_button_dx,
                pos_y=tool_button_y,
                size=(tool_button_w, tool_button_h),
                layer=8,
                text="Insert all",
                bg_color="#947432",
                icon_path=None,
                active=False
            )
            save_all = Button(
                tool_card.card_canvas,
                pos_x=tool_button_start_x + 6 * tool_button_dx,
                pos_y=tool_button_y,
                size=(tool_button_w, tool_button_h),
                layer=8,
                text="Save all",
                bg_color="#286818",
                icon_path=None,
                active=False
            )
            add_car = Button(
                tool_card.card_canvas,
                pos_x=tool_button_start_x + 7 * tool_button_dx,
                pos_y=tool_button_y,
                size=(tool_button_w, tool_button_h),
                layer=8,
                text="Add car",
                bg_color="#1E1E1E",
                icon_path=None,
                active=False
            )
            add_clock = Button(
                tool_card.card_canvas,
                pos_x=tool_button_start_x + 8 * tool_button_dx,
                pos_y=tool_button_y,
                size=(tool_button_w, tool_button_h),
                layer=8,
                text="Add clock",
                bg_color="#1E1E1E",
                icon_path=None,
                active=False
            )
            add_phone = Button(
                tool_card.card_canvas,
                pos_x=tool_button_start_x + 9 * tool_button_dx,
                pos_y=tool_button_y,
                size=(tool_button_w, tool_button_h),
                layer=8,
                text="Add phone",
                bg_color="#1E1E1E",
                icon_path=None,
                active=False
            )
            add_tgstuff = Button(
                tool_card.card_canvas,
                pos_x=tool_button_start_x + 10 * tool_button_dx,
                pos_y=tool_button_y,
                size=(tool_button_w, tool_button_h),
                layer=8,
                text="Add TGstuff",
                bg_color="#1E1E1E",
                icon_path=None,
                active=False
            )
            
            #=====================ToolsButton=================================
            button_start_y = 50
            button_dy = 60
            button_w = 120
            button_h = 40
            b1 = Button(
                card2.card_canvas,
                pos_x=40,
                pos_y=button_start_y + 0 * button_dy,
                size=(button_w, button_h),
                layer=8,
                text="Backgounds",
                bg_color="#1E1E1E",
                callback_function=lambda: self.on_folder_button_click(b1, self.folder_manager.take_background_folder),
                icon_path=None,
                active=False
            )
            b2 = Button(
                card2.card_canvas,
                pos_x=40,
                pos_y=button_start_y + 1 * button_dy,
                size=(button_w, button_h),
                layer=8,
                text="Card balance",
                bg_color="#1E1E1E",
                callback_function=lambda: self.on_folder_button_click(b2, self.folder_manager.take_items_folder),  # Assuming "Card balance" is for items
                icon_path=None,
                active=False
            )
            b3 = Button(
                card2.card_canvas,
                pos_x=40,
                pos_y=button_start_y + 2 * button_dy,
                size=(button_w, button_h),
                layer=8,
                text="Selebrity",
                bg_color="#1E1E1E",
                callback_function=lambda: self.on_folder_button_click(b3, self.folder_manager.take_celebrities_folder),
                icon_path=None,
                active=False
            )          
            b4 = Button(
                card2.card_canvas,
                pos_x=40,
                pos_y=button_start_y + 3 * button_dy,
                size=(button_w, button_h),
                layer=8,
                text="Objects",
                bg_color="#1E1E1E",
                callback_function=lambda: self.on_folder_button_click(b4, self.folder_manager.take_object_folder),
                icon_path=None,
                active=False
            )
            b5 = Button(
                card2.card_canvas,
                pos_x=40,
                pos_y=button_start_y + 4 * button_dy,
                size=(button_w, button_h),
                layer=8,
                text="File of texts",
                bg_color="#1E1E1E",
                callback_function=lambda: self.on_folder_button_click(b5, self.folder_manager.take_text_file),
                icon_path=None,
                active=False
            )
            b6 = Button(
                card2.card_canvas,
                pos_x=40,
                pos_y=button_start_y + 5 * button_dy,
                size=(button_w, button_h),
                layer=8,
                text="Cars",
                bg_color="#1E1E1E",
                callback_function=lambda: self.on_folder_button_click(b6, self.folder_manager.take_cars_folder),
                icon_path=None,
                active=False
            )
            b7 = Button(
                card2.card_canvas,
                pos_x=40,
                pos_y=button_start_y + 6 * button_dy,
                size=(button_w, button_h),
                layer=8,
                text="Clocks",
                bg_color="#1E1E1E",
                callback_function=lambda: self.on_folder_button_click(b7, self.folder_manager.take_clocks_folder),
                icon_path=None,
                active=False
            )
            b8 = Button(
                card2.card_canvas,
                pos_x=40,
                pos_y=button_start_y + 7 * button_dy,
                size=(button_w, button_h),
                layer=8,
                text="Phones",
                bg_color="#1E1E1E",
                callback_function=lambda: self.on_folder_button_click(b8, self.folder_manager.take_phones_folder),
                icon_path=None,
                active=False
            )
            b9 = Button(
                card2.card_canvas,
                pos_x=40,
                pos_y=button_start_y + 8 * button_dy,
                size=(button_w, button_h),
                layer=8,
                text="TGstuff",
                bg_color="#1E1E1E",
                callback_function=lambda: self.on_folder_button_click(b9, self.folder_manager.take_tgstuff_folder),
                icon_path=None,
                active=False
            )
            
            self.buttons = [b1, b2, b3, b4, b5, b6, b7, b8, b9] 
            
            
            self.before_canvas = Canvas(card3.card_canvas, is_before=True)
            self.after_canvas = Canvas(card4.card_canvas, is_before=False)
            
            
            choose_bg.callback_function = lambda: self.add_field_to_both('background')
            add_card_image.callback_function = lambda: self.add_field_to_both('card')
            add_selebrity.callback_function = lambda: self.add_field_to_both('celebrity')
            add_object.callback_function = lambda: self.add_field_to_both('object')
            add_text_fild.callback_function = lambda: self.add_field_to_both('text')
            add_car.callback_function = lambda: self.add_field_to_both('car')
            add_clock.callback_function = lambda: self.add_field_to_both('clock')
            add_phone.callback_function = lambda: self.add_field_to_both('phone')
            add_tgstuff.callback_function = lambda: self.add_field_to_both('tgstuff')
            insert_all.callback_function = self.insert_all
            save_all.callback_function = self.save_all
            
            choose_bg.setup_events()
            add_card_image.setup_events()
            add_selebrity.setup_events()
            add_object.setup_events()
            add_text_fild.setup_events()
            add_car.setup_events()
            add_clock.setup_events()
            add_phone.setup_events()
            add_tgstuff.setup_events()
            insert_all.setup_events()
            save_all.setup_events()
            
                        
    
    def on_folder_button_click(self, button: Button, func):
        func(button)