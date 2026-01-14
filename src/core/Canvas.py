from PIL import Image, ImageTk, ImageDraw
import tkinter as tk
from .Item import Item  # Assuming Item is in core

class Canvas:
    def __init__(self, canvas_tk: tk.Canvas):
        self.tk_canvas = canvas_tk
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
        if self.selected_item:
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
                if item.canvas_id in clicked_ids:
                    self.selected_item = item
                    if not item.is_background:  # No handles for background
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
        else:
            new_item = Item(item_type, 50 + len(self.items) * 20, 50 + len(self.items) * 20, 100, 100)
            new_item.is_background = False
        
        self.items.append(new_item)
        new_item.draw_on_canvas(self.tk_canvas)

    def insert_content(self, folder_manager):
        for item in self.items:
            paths = {
                'background': folder_manager.all_paths_to_backgrounds_images,
                'card': folder_manager.all_paths_to_items_images,
                'celebrity': folder_manager.all_paths_to_celebrities_images,
                'object': folder_manager.all_paths_to_objects_images,
                'text': folder_manager.paths_to_texts
            }.get(item.type, [])
            
            if paths:
                import random
                if item.type == 'text':
                    path = random.choice(paths)
                    with open(path, 'r') as f:
                        item.content = f.read().strip()[:100]
                else:
                    path = random.choice(paths)
                    item.content = Image.open(path)
                item.draw_on_canvas(self.tk_canvas)

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

    def _text_to_image(self, text: str) -> Image:
        img = Image.new("RGBA", (200, 50), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)
        draw.text((10, 10), text, fill="white")
        return img