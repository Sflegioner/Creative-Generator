from PIL import Image, ImageTk, ImageDraw, ImageFont
import tkinter as tk
from .Item import Item 
import os
import random

class Canvas:
    def __init__(self, canvas_tk: tk.Canvas, is_before: bool):
        self.tk_canvas = canvas_tk
        self.is_before = is_before 
        self.items = []
        self.selected_item = None
        self.drag_start_x = 0
        self.drag_start_y = 0
        self.mode = None  # 'move', 'resize', 'rotate'
        self.handle_size = 8
        self.handles = []
        self.setup_bindings()

    def setup_bindings(self):
        self.tk_canvas.bind("<Button-1>", self.on_click)
        self.tk_canvas.bind("<B1-Motion>", self.on_drag)
        self.tk_canvas.bind("<ButtonRelease-1>", self.on_release)
        self.tk_canvas.bind("<Delete>", self.on_delete)

    def on_click(self, event):
        self.tk_canvas.focus_set()

        clicked_ids = self.tk_canvas.find_overlapping(event.x - 2, event.y - 2, event.x + 2, event.y + 2)
        for hid in self.handles:
            if hid in clicked_ids:
                handle_index = self.handles.index(hid)
                if handle_index == 4: 
                    self.mode = 'rotate'
                else:
                    self.mode = 'resize'
                    self.resize_corner = handle_index  # 0: TL, 1: TR, 2: BR, 3: BL
                self.drag_start_x = event.x
                self.drag_start_y = event.y
                return

        self._select_item(event)
        if self.selected_item and not self.selected_item.is_background:
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
            delta = dx / 2
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

    def on_delete(self, event):
        if self.selected_item and not self.selected_item.is_background:
            self.tk_canvas.delete(self.selected_item.canvas_id)
            self.items.remove(self.selected_item)
            self.selected_item = None
            self.clear_handles()

    def _select_item(self, event):
        self.clear_handles()
        clicked_ids = self.tk_canvas.find_overlapping(event.x - 5, event.y - 5, event.x + 5, event.y + 5)
        
        found = False
        if clicked_ids:

            for item in reversed(self.items):
                if item.canvas_id in clicked_ids:
                    if item.is_background:
                        continue 
                    self.selected_item = item
                    self.draw_handles()
                    found = True
                    break

            if not found:
                for item in self.items:
                    if item.canvas_id in clicked_ids and item.is_background:
                         self.selected_item = None
                         break
        else:
            self.selected_item = None

    def draw_handles(self):
        if not self.selected_item:
            return
        x, y, w, h = self.selected_item.x, self.selected_item.y, self.selected_item.width // 2, self.selected_item.height // 2
        
        self.handles = [
            self.tk_canvas.create_rectangle(x - w - self.handle_size, y - h - self.handle_size, x - w + self.handle_size, y - h + self.handle_size, fill="blue"),
            self.tk_canvas.create_rectangle(x + w - self.handle_size, y - h - self.handle_size, x + w + self.handle_size, y - h + self.handle_size, fill="blue"),
            self.tk_canvas.create_rectangle(x + w - self.handle_size, y + h - self.handle_size, x + w + self.handle_size, y + h + self.handle_size, fill="blue"),
            self.tk_canvas.create_rectangle(x - w - self.handle_size, y + h - self.handle_size, x - w + self.handle_size, y + h + self.handle_size, fill="blue"),
            self.tk_canvas.create_oval(x - self.handle_size, y - h - self.handle_size - 20, x + self.handle_size, y - h + self.handle_size - 20, fill="green")
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
            new_item.is_background = True
            self.items.insert(0, new_item)
        else:
            new_item = Item(item_type, 50 + len(self.items) * 20, 50 + len(self.items) * 20, 100, 100)
            new_item.is_background = False
            self.items.append(new_item)
        
        new_item.draw_on_canvas(self.tk_canvas)
        if new_item.is_background:
            self.tk_canvas.lower(new_item.canvas_id)

    def insert_content(self, folder_manager):
        suffix = '_D' if self.is_before else '_P'
        
        for item in self.items:

            paths = {
                'background': folder_manager.all_paths_to_backgrounds_images,
                'card': folder_manager.all_paths_to_items_images,
                'celebrity': folder_manager.all_paths_to_celebrities_images,
                'object': folder_manager.all_paths_to_objects_images,
                'car': folder_manager.all_paths_to_cars_images,
                'clock': folder_manager.all_paths_to_clocks_images,
                'phone': folder_manager.all_paths_to_phones_images,
                'tgstuff': folder_manager.all_paths_to_tgstuff_images,
                'text': folder_manager.paths_to_texts
            }.get(item.type, [])

            if not paths:
                continue

            if item.type == 'text':
                path = random.choice(paths)
                valid_lines = []

                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                except UnicodeDecodeError:
                    try:
                        with open(path, 'r', encoding='cp1251') as f:
                            lines = f.readlines()
                    except Exception as e:
                        print(f"Error reading file {path}: {e}")
                        lines = []

                for line in lines:
                    clean_line = line.strip()
                    if clean_line.endswith(suffix):
                        content_without_suffix = clean_line[:-len(suffix)]
                        final_text = content_without_suffix.strip().strip('"')
                        
                        if final_text:
                            valid_lines.append(final_text)

                if valid_lines:
                    selected_text = random.choice(valid_lines)
                    item.content = self._text_to_image(selected_text)
                else:
                    print(f"No text found with suffix {suffix} in {path}")

            else:

                filtered_paths = [
                    p for p in paths 
                    if os.path.basename(p).rsplit('.', 1)[0].lower().endswith(suffix.lower())
                ]
                
                candidates = filtered_paths if filtered_paths else paths
                path = random.choice(candidates)
                
                try:
                    item.content = Image.open(path)
                except Exception as e:
                    print(f"Error opening image {path}: {e}")

            item.draw_on_canvas(self.tk_canvas)
            if item.is_background:
                self.tk_canvas.lower(item.canvas_id)

    def _text_to_image(self, text: str) -> Image:
        font_size = 40
        
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except OSError:
            try:
                font_path = "C:/GitProjects/Creative-Generator/resources/fonts/TikTokSans-VF-v3.3.ttf"
                font = ImageFont.truetype(font_path, font_size)
            except OSError:
                font = ImageFont.load_default()

        dummy = Image.new("RGBA", (1, 1))
        d = ImageDraw.Draw(dummy)
        bbox = d.textbbox((0, 0), text, font=font)
        
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        
        w = text_w + 40
        h = text_h + 40

        img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        
        x_pos, y_pos = 20, 10

        outline_color = "black"
        thickness = 2
        for x_off in range(-thickness, thickness + 1):
            for y_off in range(-thickness, thickness + 1):
                if x_off == 0 and y_off == 0:
                    continue
                d.text((x_pos + x_off, y_pos + y_off), text, font=font, fill=outline_color)

        d.text((x_pos, y_pos), text, fill="white", font=font)

        return img

    def save_composition(self, filename: str):
        width, height = self.tk_canvas.winfo_width(), self.tk_canvas.winfo_height()
        composite = Image.new("RGBA", (width, height), (0, 0, 0, 0))

        for item in self.items:
            if item.content:
                content_img = item.content if not isinstance(item.content, str) else self._text_to_image(item.content)
                rotated = content_img.rotate(item.rotation, expand=True, resample=Image.BICUBIC)
                # Змінюємо розмір
                resized = rotated.resize((item.width, item.height), Image.LANCZOS)
                
                paste_x = item.x - item.width // 2
                paste_y = item.y - item.height // 2
                
                # Накладаємо
                composite.paste(resized, (paste_x, paste_y), resized if resized.mode == 'RGBA' else None)
        
        composite.save(filename)