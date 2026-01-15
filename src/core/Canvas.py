# src/gui/canvas.py (assuming file structure)
from PIL import Image, ImageTk, ImageDraw, ImageFont
import tkinter as tk
from .Item import Item  # Assuming Item is in core, adjust if needed
import os
import random

class Canvas:
    def __init__(self, canvas_tk: tk.Canvas, is_before: bool):
        self.tk_canvas = canvas_tk
        self.is_before = is_before  # True for Before canvas (_D), False for After (_P)
        self.items = []  # List of Item objects
        self.selected_item = None
        self.drag_start_x = 0
        self.drag_start_y = 0
        self.mode = None  # 'move', 'resize', 'rotate'
        self.handle_size = 8  # Size of handle squares/circles
        self.handles = []  # List of handle IDs on canvas
        self.setup_bindings()

    def setup_bindings(self):
        self.tk_canvas.bind("<Button-1>", self.on_click)
        self.tk_canvas.bind("<B1-Motion>", self.on_drag)
        self.tk_canvas.bind("<ButtonRelease-1>", self.on_release)

    def on_click(self, event):
        # Check if clicked on a handle first
        clicked_ids = self.tk_canvas.find_overlapping(event.x - 2, event.y - 2, event.x + 2, event.y + 2)
        for hid in self.handles:
            if hid in clicked_ids:
                handle_index = self.handles.index(hid)
                if handle_index == 4:  # Rotation handle (top)
                    self.mode = 'rotate'
                else:
                    self.mode = 'resize'
                    self.resize_corner = handle_index  # 0: TL, 1: TR, 2: BR, 3: BL
                self.drag_start_x = event.x
                self.drag_start_y = event.y
                return

        # Otherwise, select item
        self._select_item(event)
        if self.selected_item and not self.selected_item.is_background:  # Ignore selection for background
            self.mode = 'move'
            self.drag_start_x = event.x
            self.drag_start_y = event.y

    def on_drag(self, event):
        if not self.selected_item:
            return

        dx = event.x - self.drag_start_x
        dy = event.y - self.drag_start_y

        if self.mode == 'move' and not self.selected_item.is_background:
            self.selected_item.update_position(self.selected_item.x + dx, self.selected_item.y + dy)
        elif self.mode == 'resize':
            self._resize_item(dx, dy)
        elif self.mode == 'rotate':
            delta = dx / 2  # Adjust sensitivity
            self.selected_item.rotate(delta)

        self.redraw_selected_item()
        self.drag_start_x = event.x
        self.drag_start_y = event.y

    def _resize_item(self, dx, dy):
        item = self.selected_item
        if self.resize_corner == 0:  # Top-left
            item.x += dx
            item.y += dy
            item.width -= dx
            item.height -= dy
        elif self.resize_corner == 1:  # Top-right
            item.y += dy
            item.width += dx
            item.height -= dy
        elif self.resize_corner == 2:  # Bottom-right
            item.width += dx
            item.height += dy
        elif self.resize_corner == 3:  # Bottom-left
            item.x += dx
            item.width -= dx
            item.height += dy
        
        item.width = max(10, item.width)
        item.height = max(10, item.height)

    def on_release(self, event):
        self.mode = None

    def _select_item(self, event):
        self.clear_handles()
        clicked_ids = self.tk_canvas.find_overlapping(event.x - 5, event.y - 5, event.x + 5, event.y + 5)
        if clicked_ids:
            for item in self.items:
                if item.canvas_id in clicked_ids and not item.is_background:  # Ignore background
                    self.selected_item = item
                    if not item.is_background:
                        self.draw_handles()
                    break
        else:
            self.selected_item = None

    def draw_handles(self):
        if not self.selected_item:
            return
        x, y, w, h = self.selected_item.x, self.selected_item.y, self.selected_item.width // 2, self.selected_item.height // 2
        # Corners: TL, TR, BR, BL
        self.handles = [
            self.tk_canvas.create_rectangle(x - w - self.handle_size, y - h - self.handle_size, x - w + self.handle_size, y - h + self.handle_size, fill="blue"),
            self.tk_canvas.create_rectangle(x + w - self.handle_size, y - h - self.handle_size, x + w + self.handle_size, y - h + self.handle_size, fill="blue"),
            self.tk_canvas.create_rectangle(x + w - self.handle_size, y + h - self.handle_size, x + w + self.handle_size, y + h + self.handle_size, fill="blue"),
            self.tk_canvas.create_rectangle(x - w - self.handle_size, y + h - self.handle_size, x - w + self.handle_size, y + h + self.handle_size, fill="blue"),
            # Rotation handle (top center)
            self.tk_canvas.create_oval(x - self.handle_size, y - h - self.handle_size - 10, x + self.handle_size, y - h + self.handle_size - 10, fill="green")
        ]

    def clear_handles(self):
        for hid in self.handles:
            self.tk_canvas.delete(hid)
        self.handles = []

    def redraw_selected_item(self):
        if self.selected_item:
            self.selected_item.draw_on_canvas(self.tk_canvas)
            self.clear_handles()
            if not self.selected_item.is_background:
                self.draw_handles()

    def add_item(self, item_type: str):
        if item_type == 'background':
            width = self.tk_canvas.winfo_width()
            height = self.tk_canvas.winfo_height()
            new_item = Item(item_type, width // 2, height // 2, width, height)
            new_item.is_background = True  # Flag to disable manipulation
            self.items.insert(0, new_item)  # Add to beginning for lowest layer
        else:
            new_item = Item(item_type, 50 + len(self.items) * 20, 50 + len(self.items) * 20, 100, 100)
            new_item.is_background = False
            self.items.append(new_item)
        
        new_item.draw_on_canvas(self.tk_canvas)
        if new_item.is_background:
            self.tk_canvas.lower(new_item.canvas_id)  # Send to back

    def insert_content(self, folder_manager):
        suffix = '_D' if self.is_before else '_P'
        for item in self.items:
            paths = {
                'background': folder_manager.all_paths_to_backgrounds_images,
                'card': folder_manager.all_paths_to_items_images,
                'celebrity': folder_manager.all_paths_to_celebrities_images,
                'object': folder_manager.all_paths_to_objects_images,
                'text': folder_manager.paths_to_texts
            }.get(item.type, [])
            
            if paths:
                # Filter paths that end with the suffix before the extension (case-insensitive)
                filtered_paths = [
                    p for p in paths 
                    if os.path.basename(p).rsplit('.', 1)[0].lower().endswith(suffix.lower())
                ]
                if item.type == 'text':
                    print(f"Suffix for text: {suffix}")
                    print(f"All text paths: {paths}")
                    print(f"Filtered text paths: {filtered_paths}")
                if not filtered_paths:
                    filtered_paths = paths  # Fallback to all if none match
                
                path = random.choice(filtered_paths)
                if item.type == 'text':
                    try:
                        with open(path, 'r', encoding='utf-8') as f:
                            item.content = f.read().strip()
                    except UnicodeDecodeError:
                        with open(path, 'r', encoding='cp1251') as f:
                            item.content = f.read().strip()  # Fallback to cp1251 for Windows Cyrillic files
                else:
                    item.content = Image.open(path)
                item.draw_on_canvas(self.tk_canvas)
                if item.is_background:
                    self.tk_canvas.lower(item.canvas_id)  # Ensure background stays at back after insert

    def save_composition(self, filename: str):
        width, height = self.tk_canvas.winfo_width(), self.tk_canvas.winfo_height()
        composite = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        for item in self.items:
            if item.content:
                content = item.content if not isinstance(item.content, str) else self._text_to_image(item.content)
                rotated = content.rotate(item.rotation, expand=True)
                resized = rotated.resize((item.width, item.height))
                paste_x = item.x - item.width // 2
                paste_y = item.y - item.height // 2
                composite.paste(resized, (paste_x, paste_y), resized if resized.mode == 'RGBA' else None)
        composite.save(filename)

    def insert_content(self, folder_manager):
        suffix = '_D' if self.is_before else '_P'

        for item in self.items:
            if item.type != 'text':
                continue
            paths = folder_manager.paths_to_texts
            if not paths:
                continue

            path = random.choice(paths) 
            lines = []

            try:
                with open(path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
            except UnicodeDecodeError:
                with open(path, 'r', encoding='cp1251') as f:
                    lines = f.readlines()


            selected_line = None
            for line in lines:
                clean = line.strip()
                if not clean:
                    continue

                if clean.endswith(suffix):
                    selected_line = clean.replace(suffix, "").strip()
                    break

            if not selected_line:
                selected_line = lines[0].strip() if lines else ""

            item.content = selected_line
            item.draw_on_canvas(self.tk_canvas)

    def _text_to_image(self, text: str) -> Image:
        font_size = 20
        font_path = "C:/GitProjects/Creative-Generator/resources/fonts/TikTokSans-VF-v3.3.ttf"

        font = ImageFont.truetype(font_path, font_size)

        dummy = Image.new("RGBA", (1, 1))
        d = ImageDraw.Draw(dummy)
        bbox = d.textbbox((0, 0), text, font=font)

        w = bbox[2] - bbox[0] + 20
        h = bbox[3] - bbox[1] + 20

        img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        d.text((10, 10), text, fill="white", font=font)

        return img
