from PIL import Image, ImageTk, ImageDraw
import math

class Item:
    def __init__(self, item_type: str, pos_x: int, pos_y: int, width: int, height: int, rotation: float = 0.0):
        self.type = item_type  # 'background', 'card', 'celebrity', 'object', 'text'
        self.x = pos_x
        self.y = pos_y
        self.width = width
        self.height = height
        self.rotation = rotation
        self.content = None  # Will be PIL Image or str (for text)
        self.canvas_id = None  # Tk canvas item ID for placeholder/image
        self.photo = None  # ImageTk.PhotoImage for display
        self.is_background = False  # Flag for special handling
        self.tk_image = None

    def draw_on_canvas(self, tk_canvas: tk.Canvas, bg_color: str = "#808080"):
        """Draw placeholder rectangle or actual content if loaded."""
        if isinstance(self.content, Image.Image):
            self.tk_image = ImageTk.PhotoImage(self.content)

            if self.canvas_id:
                tk_canvas.itemconfig(self.canvas_id, image=self.tk_image)
            else:
                self.canvas_id = tk_canvas.create_image(
                    self.x, self.y,
                    image=self.tk_image
            )
        
        if self.canvas_id:
            tk_canvas.delete(self.canvas_id)
        
        center_x, center_y = self.x, self.y
        half_w, half_h = self.width // 2, self.height // 2
        
        if self.content:  # If inserted, draw rotated image
            if isinstance(self.content, str):  # Text
                rotated_img = self._rotate_text(self.content)
            else:  # Image
                rotated_img = self.content.rotate(self.rotation, expand=True).resize((self.width, self.height))
            self.photo = ImageTk.PhotoImage(rotated_img)
            self.canvas_id = tk_canvas.create_image(center_x, center_y, image=self.photo, anchor="center")
        else:  # Placeholder
            points = self._get_rotated_rect_points(center_x, center_y, half_w, half_h, self.rotation)
            self.canvas_id = tk_canvas.create_polygon(points, fill=bg_color, outline="#FFFFFF")

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

    def _rotate_text(self, text: str) -> Image:
        temp_img = Image.new("RGBA", (self.width, self.height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(temp_img)
        draw.text((10, 10), text, fill="white")
        return temp_img.rotate(self.rotation, expand=True)

    def update_position(self, new_x: int, new_y: int):
        self.x = new_x
        self.y = new_y

    def resize(self, new_width: int, new_height: int):
        self.width = max(10, new_width)
        self.height = max(10, new_height)

    def rotate(self, delta: float):
        self.rotation = (self.rotation + delta) % 360