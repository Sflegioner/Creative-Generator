import tkinter as tk
from tkinter import ttk
import os
from PIL import ImageFont

class FontSelector:
    def __init__(self, parent_canvas: tk.Canvas, initial_font: str = "arial.ttf", fonts_dir: str = "C:/GitProjects/Creative-Generator/resources/fonts"):
        self.parent_canvas = parent_canvas
        self.fonts_dir = fonts_dir
        self.available_fonts = self._load_available_fonts()
        self.selected_font = initial_font if initial_font in self.available_fonts else self.available_fonts[0] if self.available_fonts else "arial.ttf"
        self.combobox = ttk.Combobox(self.parent_canvas, values=self.available_fonts, state="readonly", width=20)
        self.combobox.set(self.selected_font)
        self.combobox.bind("<<ComboboxSelected>>", self._on_select)
        self.combobox.place(x=10, y=10)  

    def _load_available_fonts(self):
        """Scan the fonts directory for .ttf files."""
        if not os.path.exists(self.fonts_dir):
            return ["arial.ttf"]  
        
        fonts = []
        for file in os.listdir(self.fonts_dir):
            if file.lower().endswith('.ttf'):
                full_path = os.path.join(self.fonts_dir, file)
                try:
                    ImageFont.truetype(full_path, 40)
                    fonts.append(file) 
                except Exception:
                    pass  
        return fonts if fonts else ["arial.ttf"]

    def _on_select(self, event):
        """Update the selected font when changed."""
        self.selected_font = self.combobox.get()
        print(f"Selected font: {self.selected_font}") 

    def get_selected_font_path(self):
        """Get the full path to the selected font."""
        return os.path.join(self.fonts_dir, self.selected_font)