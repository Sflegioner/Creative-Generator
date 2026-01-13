import tkinter as tk

class Button:
    """
    Colors:
        #3B3B3B          - default card bg
        #8F7FFF          - header text color (purple)
        #1E1E1E          - header bg
    """
    
    def __init__(self,
                 root: tk.Tk | tk.Canvas, 
                 pos_x: int,
                 pos_y: int,
                 size: tuple[int, int],
                 layer: int,
                 text: str | None = None,
                 bg_color: str = "#474747",
                 callback_function: callable | None = None,
                 icon_path: str | None = None,
                 active: bool = False
                 ):          
    
        self.root = root  
        self.x = pos_x
        self.y = pos_y
        self.width, self.height = size
        self.layer = layer  
        self.text = text
        self.bg_color = bg_color
        self.callback_function = callback_function
        self.icon_path = icon_path
        self.active = active
        self.tag = f"button_{id(self)}"
        self.rect_id = None
        self.text_id = None
        self.icon_id = None
        self.icon = None

        self.draw_self()
        self.setup_events()
        if self.active:
            self.draw_if_active()
        
    def draw_self(self):
        self.rect_id = self.root.create_rectangle(
            self.x, self.y, self.x + self.width, self.y + self.height,
            fill=self.bg_color, outline="", width=0, tags=self.tag
        )
        if self.icon_path:
            self.draw_icon()
        if self.text:
            self.draw_text()
    
    def draw_text(self):
        y_offset = 0
        if self.icon_path and self.icon:
            y_offset = self.icon.height() // 2 + 10
        
        self.text_id = self.root.create_text(
            self.x + self.width // 2,
            self.y + self.height // 2 + y_offset,
            text=self.text,
            fill="#8F7FFF",
            font=("Arial", 12),  
            anchor="center",
            tags=self.tag
        )
    
    def draw_icon(self):
        """
        Draw icon if needed
        """
        self.icon = tk.PhotoImage(file=self.icon_path)
        y_offset = 0
        if self.text:
            # Shift icon up if text is present to avoid overlap
            y_offset = - (self.icon.height() // 2 + 10) // 2  # Rough adjustment
        
        self.icon_id = self.root.create_image(
            self.x + self.width // 2,
            self.y + self.height // 2 + y_offset,
            image=self.icon,
            anchor="center",
            tags=self.tag
        )
    
    def setup_events(self):
        if self.callback_function:
            self.root.tag_bind(self.tag, "<Button-1>", self.on_click)
        self.root.tag_bind(self.tag, "<Enter>", self.on_enter)
        self.root.tag_bind(self.tag, "<Leave>", self.on_leave)
    
    def on_click(self, event):
        if self.callback_function:
            self.callback_function()
    
    def on_enter(self, event):
        if self.rect_id:
            self.root.itemconfig(self.rect_id, fill="#3F3743")  
    
    def on_leave(self, event):
        if self.rect_id:
            self.root.itemconfig(self.rect_id, fill=self.bg_color)
    
    
    def draw_if_active(self):
        if self.rect_id:
            if self.active:
                self.root.itemconfig(self.rect_id, outline="#8F7FFF", width=2)  # Active highlight
            else:
                self.root.itemconfig(self.rect_id, outline="", width=0)
    
    def set_active(self, active: bool = True):
        self.active = active
        self.draw_if_active()