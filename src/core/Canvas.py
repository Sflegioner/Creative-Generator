# core/Canvas.py
from PIL import Image, ImageTk, ImageDraw, ImageFont, ImageFilter
import tkinter as tk
from tkinter import simpledialog 
from .Item import Item 
import os
import random

class Canvas:
    
    def __init__(self, canvas_tk: tk.Canvas, is_before: bool, main_window):
        self.tk_canvas = canvas_tk
        self.is_before = is_before 
        self.main_window = main_window
        self.items = []
        self.selected_item = None
        self.drag_start_x = 0
        self.drag_start_y = 0
        self.mode = None  
        self.handle_size = 8
        self.handles = []
        self.preview_mode = False
        self.setup_bindings()

    def setup_bindings(self):
        self.tk_canvas.bind("<Button-1>", self.on_click)
        self.tk_canvas.bind("<B1-Motion>", self.on_drag)
        self.tk_canvas.bind("<ButtonRelease-1>", self.on_release)
        self.tk_canvas.bind("<Delete>", self.on_delete)
        self.tk_canvas.bind("<Double-Button-1>", self.on_double_click) 

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
                    self.resize_corner = handle_index
                self.drag_start_x = event.x
                self.drag_start_y = event.y
                self.preview_mode = True
                return

        self._select_item(event)
        if self.selected_item and not self.selected_item.is_background:
            self.mode = 'move'
            self.drag_start_x = event.x
            self.drag_start_y = event.y
            self.preview_mode = True

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
        self.preview_mode = False
        self.mode = None
        if self.selected_item:
            self.redraw_selected_item()

    def on_delete(self, event):
        if self.selected_item and not self.selected_item.is_background:
            self.tk_canvas.delete(self.selected_item.canvas_id)
            self.items.remove(self.selected_item)
            self.selected_item = None
            self.clear_handles()

    def on_double_click(self, event):
        if not self.selected_item or self.selected_item.type != 'text':
            return

        new_text = simpledialog.askstring(
            "Edit",
            "New text:",
            initialvalue=self.selected_item.text or ""
        )

        if new_text is not None:  
            self.selected_item.text = new_text
            font_path = self.main_window.font_selector.get_selected_font_path()

            display_text = new_text if new_text.strip() else " "
            self.selected_item.content = self._text_to_image(display_text, font_path=font_path)
            self.selected_item.preview_content = None
            self.redraw_selected_item()

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
            self.selected_item.draw_on_canvas(self.tk_canvas, use_preview=self.preview_mode)
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
            if item_type == 'text':
                new_item.text = ""
            self.items.append(new_item)
        
        new_item.draw_on_canvas(self.tk_canvas)
        if new_item.is_background:
            self.tk_canvas.lower(new_item.canvas_id)

    def insert_content(self, folder_manager):
        suffix = '_D' if self.is_before else '_P'
        preferred_suffix = suffix
        
        folder_manager.reload_all_paths()

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
                # Текстова логіка без змін
                if not hasattr(folder_manager, 'text_pairs'):
                    text_pairs = {}
                    for path in paths:
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
                            if not clean_line:
                                continue
                            split_str = None
                            current_suffix = None
                            if '_D ' in clean_line:
                                split_str = '_D '
                                current_suffix = '_D'
                            elif '_P ' in clean_line:
                                split_str = '_P '
                                current_suffix = '_P'
                            if split_str is None:
                                continue
                            parts = clean_line.rsplit(split_str, 1)
                            if len(parts) != 2:
                                continue
                            phrase = parts[0].strip().strip('"')
                            id_str = parts[1].strip()
                            if not id_str.isdigit():
                                continue
                            id_num = int(id_str)
                            if id_num not in text_pairs:
                                text_pairs[id_num] = {}
                            text_pairs[id_num][current_suffix] = phrase
                    
                    folder_manager.text_pairs = text_pairs
                else:
                    text_pairs = folder_manager.text_pairs

                if self.is_before or not hasattr(folder_manager, 'selected_text_id'):
                    complete_ids = [id_num for id_num, d in text_pairs.items() if '_D' in d and '_P' in d]
                    if not complete_ids:
                        print("No complete text pairs found.")
                        selected_id = None
                    else:
                        selected_id = random.choice(complete_ids)
                        folder_manager.selected_text_id = selected_id
                else:
                    selected_id = folder_manager.selected_text_id

                font_path = self.main_window.font_selector.get_selected_font_path()

                if (selected_id is not None and 
                    selected_id in text_pairs and 
                    suffix in text_pairs[selected_id]):
                    selected_text = text_pairs[selected_id][suffix]
                    item.text = selected_text
                    item.content = self._text_to_image(selected_text, font_path=font_path)
                else:
                    print(f"No text found for ID {selected_id} and suffix {suffix}")
                    item.text = "NO TEXT"
                    item.content = self._text_to_image("NO TEXT", font_path=font_path)

                item.preview_content = None

            else:
                # Логіка для зображень (парний вибір)
                pairs = {}
                for p in paths:
                    filename = os.path.basename(p)
                    name, _ = os.path.splitext(filename)
                    parts = name.rsplit('_', 1)
                    if len(parts) == 2:
                        base, suf = parts
                        if suf.upper() in ('D', 'P'):
                            suffix_key = '_' + suf.upper()
                            pairs.setdefault(base, {})[suffix_key] = p
                            continue
                    pairs.setdefault(name, {})[''] = p

                complete_bases = [b for b in pairs if '_D' in pairs[b] and '_P' in pairs[b]]

                attr_name = f"selected_{item.type}_base"

                if self.is_before or not hasattr(folder_manager, attr_name):
                    if complete_bases:
                        chosen_base = random.choice(complete_bases)
                    else:
                        chosen_base = random.choice(list(pairs.keys()))
                    setattr(folder_manager, attr_name, chosen_base)
                else:
                    chosen_base = getattr(folder_manager, attr_name)

                base_dict = pairs[chosen_base]
                path = base_dict.get(preferred_suffix) or random.choice(list(base_dict.values()))

                try:
                    img = Image.open(path).convert("RGBA")
                    item.content = img

                    preview = img.copy()
                    preview.thumbnail((512, 512))
                    item.preview_content = preview
                except Exception as e:
                    print(f"Error opening image {path}: {e}")

            item.draw_on_canvas(self.tk_canvas)
            if item.is_background:
                self.tk_canvas.lower(item.canvas_id)
    def _text_to_image(self, text: str, font_path: str = None) -> Image:
            if not text.strip():
                text = " "

            supersample = 4
            base_font_size = 40

            if font_path:
                try:
                    temp_font = ImageFont.truetype(font_path, base_font_size)
                except OSError:
                    temp_font = ImageFont.load_default()
            else:
                try:
                    temp_font = ImageFont.truetype("arial.ttf", base_font_size)
                except OSError:
                    temp_font = ImageFont.load_default()

            dummy = Image.new("RGBA", (1, 1))
            d = ImageDraw.Draw(dummy)
            bbox = d.textbbox((0, 0), text, font=temp_font)
            base_text_w = bbox[2] - bbox[0]
            base_text_h = bbox[3] - bbox[1]

            # Більше відступів під тінь + outline
            base_w = base_text_w + 120  
            base_h = base_text_h + 120

            font_size = base_font_size * supersample

            if font_path:
                try:
                    font = ImageFont.truetype(font_path, font_size)
                except OSError:
                    font = ImageFont.load_default()
            else:
                try:
                    font = ImageFont.truetype("arial.ttf", font_size)
                except OSError:
                    font = ImageFont.load_default()

            large_w = base_w * supersample
            large_h = base_h * supersample

            # Основне зображення (прозоре)
            img_large = Image.new("RGBA", (large_w, large_h), (0, 0, 0, 0))

            # Позиція тексту
            x_pos = 60 * supersample
            y_pos = 50 * supersample

            # === ТІНЬ ===
            shadow_offset_x = supersample * 5   # вправо
            shadow_offset_y = supersample * 7   # вниз
            shadow_radius = supersample * 5     # м'якше розмиття
            shadow_color = (0, 0, 0, 220)

            shadow_layer = Image.new("RGBA", img_large.size, (0, 0, 0, 0))
            shadow_draw = ImageDraw.Draw(shadow_layer)
            shadow_draw.text(
                (x_pos + shadow_offset_x, y_pos + shadow_offset_y),
                text,
                font=font,
                fill=shadow_color
            )
            blurred_shadow = shadow_layer.filter(ImageFilter.GaussianBlur(radius=shadow_radius))
            img_large = Image.alpha_composite(img_large, blurred_shadow)

            draw = ImageDraw.Draw(img_large)

            outline_thickness = 3 * supersample  
            outline_color = (0, 0, 0, 255)       

            for dx in range(-outline_thickness, outline_thickness + 1):
                for dy in range(-outline_thickness, outline_thickness + 1):
                    if dx != 0 or dy != 0:  
                        draw.text((x_pos + dx, y_pos + dy), text, font=font, fill=outline_color)


            draw.text((x_pos, y_pos), text, fill="white", font=font)

            img = img_large.resize((base_w, base_h), Image.LANCZOS)

            return img
    def save_composition(self, filename: str):
        width, height = self.tk_canvas.winfo_width(), self.tk_canvas.winfo_height()
        composite = Image.new("RGB", (width, height), (128, 128, 128))

        for item in self.items:
            if item.content:
                content_img = item.content
                
                upscale_factor = 4
                if item.type != 'text':
                    orig_w, orig_h = content_img.size
                    supersampled = content_img.resize((orig_w * upscale_factor, orig_h * upscale_factor), Image.LANCZOS)
                    rotated = supersampled.rotate(item.rotation, expand=True, resample=Image.BICUBIC)
                else:
                    rotated = content_img.rotate(item.rotation, expand=True, resample=Image.BICUBIC)
                
                resized = rotated.resize((item.width, item.height), Image.LANCZOS)
                
                paste_x = item.x - item.width // 2
                paste_y = item.y - item.height // 2
                
                composite.paste(resized, (paste_x, paste_y), resized if resized.mode == 'RGBA' else None)
        
        composite.save(filename)