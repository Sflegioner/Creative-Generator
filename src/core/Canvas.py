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
        self.update_button_id = None        # прямокутник кнопки
        self.update_button_text_id = None   # текст кнопки (нова змінна)
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
        
        # === КЛІК ПО КНОПЦІ UPDATE (працює і по прямокутнику, і по тексту) ===
        if (self.update_button_id and self.update_button_id in clicked_ids) or \
           (self.update_button_text_id and self.update_button_text_id in clicked_ids):
            self.update_selected_item()
            return

        for hid in self.handles:
            if hid in clicked_ids:
                handle_index = self.handles.index(hid)
                if handle_index == 4:          # зелений овал — ротація
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
        if self.resize_corner == 0:   # Top-left
            item.x += dx
            item.y += dy
            item.width -= dx
            item.height -= dy
        elif self.resize_corner == 1: # Top-right
            item.y += dy
            item.width += dx
            item.height -= dy
        elif self.resize_corner == 2: # Bottom-right
            item.width += dx
            item.height += dy
        elif self.resize_corner == 3: # Bottom-left
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
            self.selected_item.content = self._text_to_image(display_text, font_path=font_path, scale_factor=1.0)
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
        if not self.selected_item or self.selected_item.is_background:
            return
        x, y = self.selected_item.x, self.selected_item.y
        w = self.selected_item.width // 2
        h = self.selected_item.height // 2
        self.handles = [
            self.tk_canvas.create_rectangle(x - w - self.handle_size, y - h - self.handle_size, x - w + self.handle_size, y - h + self.handle_size, fill="blue"),
            self.tk_canvas.create_rectangle(x + w - self.handle_size, y - h - self.handle_size, x + w + self.handle_size, y - h + self.handle_size, fill="blue"),
            self.tk_canvas.create_rectangle(x + w - self.handle_size, y + h - self.handle_size, x + w + self.handle_size, y + h + self.handle_size, fill="blue"),
            self.tk_canvas.create_rectangle(x - w - self.handle_size, y + h - self.handle_size, x - w + self.handle_size, y + h + self.handle_size, fill="blue"),
            # Green rotate handle
            self.tk_canvas.create_oval(x - self.handle_size, y - h - self.handle_size - 25,
                                      x + self.handle_size, y - h + self.handle_size - 25, fill="#4CAF50", outline="white")
        ]
        # === КНОПКА UPDATE (біля rotate) ===
        btn_x = x + 45
        btn_y = y - h - 25
        
        self.update_button_id = self.tk_canvas.create_rectangle(
            btn_x - 20, btn_y - 16, btn_x + 20, btn_y + 16,
            fill="#2196F3", outline="#FFFFFF", width=3
        )
        self.update_button_text_id = self.tk_canvas.create_text(
            btn_x, btn_y, 
            text="↻ UPDATE", 
            fill="white",
            font=("Arial", 10, "bold")   # трохи більший шрифт
        )
        
        self.handles.append(self.update_button_id)
        self.handles.append(self.update_button_text_id)

    def clear_handles(self):
        for hid in self.handles:
            self.tk_canvas.delete(hid)
        self.handles = []
        self.update_button_id = None
        self.update_button_text_id = None   # важливо!

    def redraw_selected_item(self):
        if self.selected_item:
            self.selected_item.draw_on_canvas(self.tk_canvas, use_preview=self.preview_mode)
            self.clear_handles()
            if not self.selected_item.is_background:
                self.draw_handles()

    def update_selected_item(self):
        """Оновлює ТІЛЬКИ вибраний item"""
        if not self.selected_item or self.selected_item.is_background:
            return
        try:
            self.insert_content(self.main_window.folder_manager, target_item=self.selected_item)
            self.redraw_selected_item()
            print(f"✓ Оновлено item: {self.selected_item.type} (ID: {id(self.selected_item)})")
        except Exception as e:
            print(f"Помилка оновлення item: {e}")

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

    def insert_content(self, folder_manager, target_item=None):
        """Оновлює всі items або тільки один (target_item)"""
        suffix = '_D' if self.is_before else '_P'
        preferred_suffix = suffix
       
        folder_manager.reload_all_paths()
        items_to_process = [target_item] if target_item is not None else self.items
        for item in items_to_process:
            if item is None:
                continue
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
                # ТЕКСТ
                if not hasattr(folder_manager, 'text_pairs'):
                    text_pairs = {}
                    for path in paths:
                        try:
                            with open(path, 'r', encoding='utf-8') as f:
                                lines = f.readlines()
                        except UnicodeDecodeError:
                            with open(path, 'r', encoding='cp1251') as f:
                                lines = f.readlines()
                        for line in lines:
                            clean_line = line.strip()
                            if not clean_line: continue
                            if '_D ' in clean_line:
                                split_str, cur_suf = '_D ', '_D'
                            elif '_P ' in clean_line:
                                split_str, cur_suf = '_P ', '_P'
                            else: continue
                            parts = clean_line.rsplit(split_str, 1)
                            if len(parts) != 2: continue
                            phrase = parts[0].strip().strip('"')
                            id_str = parts[1].strip()
                            if not id_str.isdigit(): continue
                            id_num = int(id_str)
                            text_pairs.setdefault(id_num, {})[cur_suf] = phrase
                    folder_manager.text_pairs = text_pairs
                else:
                    text_pairs = folder_manager.text_pairs
                # При update — завжди новий текст
                if self.is_before or not hasattr(folder_manager, 'selected_text_id') or target_item is not None:
                    complete_ids = [id_num for id_num, d in text_pairs.items() if '_D' in d and '_P' in d]
                    selected_id = random.choice(complete_ids) if complete_ids else None
                    if selected_id:
                        folder_manager.selected_text_id = selected_id
                else:
                    selected_id = getattr(folder_manager, 'selected_text_id', None)
                font_path = self.main_window.font_selector.get_selected_font_path()
                if selected_id is not None and selected_id in text_pairs and suffix in text_pairs[selected_id]:
                    selected_text = text_pairs[selected_id][suffix]
                    item.text = selected_text
                    item.content = self._text_to_image(selected_text, font_path=font_path, scale_factor=1.0)
                else:
                    item.text = "NO TEXT"
                    item.content = self._text_to_image("NO TEXT", font_path=font_path, scale_factor=1.0)
                item.preview_content = None
            else:
                # КАРТИНКИ
                pairs = {}
                for p in paths:
                    filename = os.path.basename(p)
                    name, _ = os.path.splitext(filename)
                    parts = name.rsplit('_', 1)
                    if len(parts) == 2 and parts[1].upper() in ('D', 'P'):
                        base, suf = parts
                        pairs.setdefault(base, {})['_' + suf.upper()] = p
                    else:
                        pairs.setdefault(name, {})[''] = p
                complete_bases = [b for b in pairs if '_D' in pairs[b] and '_P' in pairs[b]]
                attr_name = f"selected_{item.type}_base"
                if self.is_before or not hasattr(folder_manager, attr_name) or target_item is not None:
                    chosen_base = random.choice(complete_bases) if complete_bases else (random.choice(list(pairs.keys())) if pairs else None)
                    setattr(folder_manager, attr_name, chosen_base)
                else:
                    chosen_base = getattr(folder_manager, attr_name)
                if chosen_base and chosen_base in pairs:
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

    def _text_to_image(self, text: str, font_path: str = None, scale_factor: float = 1.0) -> Image:
        if not text.strip():
            text = " "
        base_font_size = 40
       
        if scale_factor > 1.5:
            render_scale = scale_factor
            do_downscale = False
        else:
            render_scale = 4.0
            do_downscale = True
        font_size = int(base_font_size * render_scale)
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
        dummy = Image.new("RGBA", (1, 1))
        d = ImageDraw.Draw(dummy)
        bbox = d.textbbox((0, 0), text, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        padding = int(30 * render_scale)
        img_w = text_w + padding * 2
        img_h = text_h + padding * 2
        img = Image.new("RGBA", (img_w, img_h), (0, 0, 0, 0))
       
        x_pos = padding
        y_pos = padding
        # ТІНЬ
        shadow_offset_x = int(5 * render_scale)
        shadow_offset_y = int(7 * render_scale)
        shadow_radius = int(5 * render_scale)
        shadow_color = (0, 0, 0, 220)
        shadow_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
        shadow_draw = ImageDraw.Draw(shadow_layer)
        shadow_draw.text((x_pos + shadow_offset_x, y_pos + shadow_offset_y), text, font=font, fill=shadow_color)
        blurred_shadow = shadow_layer.filter(ImageFilter.GaussianBlur(radius=shadow_radius))
        img = Image.alpha_composite(img, blurred_shadow)
        draw = ImageDraw.Draw(img)
        # OUTLINE
        outline_thickness = int(3 * render_scale)
        outline_color = (0, 0, 0, 255)
        for dx in range(-outline_thickness, outline_thickness + 1):
            for dy in range(-outline_thickness, outline_thickness + 1):
                if dx != 0 or dy != 0:
                    draw.text((x_pos + dx, y_pos + dy), text, font=font, fill=outline_color)
        # Основний текст
        draw.text((x_pos, y_pos), text, fill="white", font=font)
        if do_downscale:
            target_w = int(img_w / 4)
            target_h = int(img_h / 4)
            img = img.resize((target_w, target_h), Image.LANCZOS)
        return img

    def save_composition(self, filename: str):
        SAVE_SCALE = 4.0
        canvas_w = self.tk_canvas.winfo_width()
        canvas_h = self.tk_canvas.winfo_height()
        target_w = int(canvas_w * SAVE_SCALE)
        target_h = int(canvas_h * SAVE_SCALE)
        composite = Image.new("RGB", (target_w, target_h), (128, 128, 128))
        font_path = self.main_window.font_selector.get_selected_font_path()
        for item in self.items:
            center_x = item.x * SAVE_SCALE
            center_y = item.y * SAVE_SCALE
            target_item_w = int(item.width * SAVE_SCALE)
            target_item_h = int(item.height * SAVE_SCALE)
            img_to_paste = None
            if item.type == 'text':
                high_res_text = self._text_to_image(item.text, font_path=font_path, scale_factor=SAVE_SCALE)
                rotated = high_res_text.rotate(item.rotation, expand=True, resample=Image.BICUBIC)
                img_to_paste = rotated.resize((target_item_w, target_item_h), Image.LANCZOS)
            elif item.content:
                original_img = item.content
                rotated = original_img.rotate(item.rotation, expand=True, resample=Image.BICUBIC)
                img_to_paste = rotated.resize((target_item_w, target_item_h), Image.LANCZOS)
            if img_to_paste:
                paste_w, paste_h = img_to_paste.size
                paste_x = int(center_x - paste_w / 2)
                paste_y = int(center_y - paste_h / 2)
                if img_to_paste.mode == 'RGBA':
                    composite.paste(img_to_paste, (paste_x, paste_y), img_to_paste)
                else:
                    composite.paste(img_to_paste, (paste_x, paste_y))
       
        composite.save(filename, quality=95, subsampling=0)