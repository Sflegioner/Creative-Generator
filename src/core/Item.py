from PIL import Image, ImageTk, ImageDraw
import math
import tkinter as tk 

class Item:
    def __init__(self, item_type: str, pos_x: int, pos_y: int, width: int, height: int, rotation: float = 0.0):
        self.type = item_type  
        self.x = pos_x
        self.y = pos_y
        self.width = width
        self.height = height
        self.rotation = rotation
        self.content = None         
        self.preview_content = None 
        self.canvas_id = None  
        self.photo = None  
        self.is_background = False  
        self.tk_image = None
        self.text: str = ""  

    def draw_on_canvas(self, tk_canvas: tk.Canvas, bg_color: str = "#808080", use_preview: bool = False):
        if self.canvas_id:
            tk_canvas.delete(self.canvas_id)
        content_to_use = self.preview_content if use_preview and self.preview_content is not None else self.content

        if content_to_use:
            try:
                rotated_img = content_to_use.rotate(self.rotation, expand=True, resample=Image.BICUBIC)
                resized_img = rotated_img.resize((self.width, self.height), Image.LANCZOS)
                self.photo = ImageTk.PhotoImage(resized_img)
            
                self.canvas_id = tk_canvas.create_image(
                    self.x, self.y, 
                    image=self.photo, 
                    anchor="center"
                )
            except Exception as e:
                self._draw_placeholder(tk_canvas, bg_color)
        else:
            self._draw_placeholder(tk_canvas, bg_color)

    def _draw_placeholder(self, tk_canvas, bg_color):
        half_w, half_h = self.width // 2, self.height // 2
        points = self._get_rotated_rect_points(self.x, self.y, half_w, half_h, self.rotation)
        self.canvas_id = tk_canvas.create_polygon(
            points, 
            fill=bg_color, 
            outline="#FFFFFF", 
            width=2
        )

    def _get_rotated_rect_points(self, cx, cy, hw, hh, angle):
        angle_rad = math.radians(angle)
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)
        
        corners = [(-hw, -hh), (hw, -hh), (hw, hh), (-hw, hh)]
        rotated_points = []
        for dx, dy in corners:
            rx = cx + dx * cos_a - dy * sin_a
            ry = cy + dx * sin_a + dy * cos_a
            rotated_points.extend([rx, ry])
        return rotated_points

    def update_position(self, new_x: int, new_y: int):
        self.x = new_x
        self.y = new_y

    def rotate(self, delta: float):
        self.rotation = (self.rotation + delta) % 360