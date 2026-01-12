# TODO: change * import 
from tkinter import Tk, Canvas, Misc

class Card:
    """
    Colors:
        #3B3B3B          - default card bg
        #303030          - dark shadow
        #8F7FFF          - header text color (purple)
        #1E1E1E          - header bg
    """
    def __init__(self,
                 root: Tk,
                 pos_x: int,
                 pos_y: int,
                 size: tuple[int, int],
                 layer: int,
                 text: str | None = None,
                 bg_color: str = "#3B3B3B"):          
        
        self.root = root
        self.x = pos_x
        self.y = pos_y
        self.width, self.height = size
        self.layer = layer
        self.text = text
        self.bg_color = bg_color

        self.draw_self()

    def draw_self(self):
        root_bg = self.root.cget("bg")
        radius = 16
        shadow_offset_x = 5
        shadow_offset_y = 6
        shadow_extra = 8
        shadow_width = self.width + shadow_extra
        shadow_height = self.height + shadow_extra
        shadow_bg = "#141313"
        shadow_border = "#0A0A0A"
        shadow_border_width = 2
        header_bg = "#1E1E1E"
        header_fg = "#8F7FFF"
        header_height = 38
        card_border = "#4A4A4A"
        card_border_width = 1

        # Shadow canvas
        self.shadow_canvas = Canvas(
            self.root,
            width=shadow_width,
            height=shadow_height,
            bg=root_bg,
            highlightthickness=0,
            bd=0
        )
        self.shadow_canvas.place(x=self.x + shadow_offset_x, y=self.y + shadow_offset_y)

        self._draw_rounded_rect(
            self.shadow_canvas,
            0,
            0,
            shadow_width,
            shadow_height,
            radius,
            fill=shadow_bg,
            outline=shadow_border,
            line_width=shadow_border_width
        )

        # Main card canvas
        self.card_canvas = Canvas(
            self.root,
            width=self.width,
            height=self.height,
            bg=root_bg,
            highlightthickness=0,
            bd=0
        )
        self.card_canvas.place(x=self.x, y=self.y)

        # Draw header fill (top rounded part)
        self.card_canvas.create_rectangle(radius, 0, self.width - radius, header_height, fill=header_bg, outline="")
        self.card_canvas.create_rectangle(0, radius, self.width, header_height, fill=header_bg, outline="")
        self.card_canvas.create_oval(0, 0, radius * 2, radius * 2, fill=header_bg, outline="")
        self.card_canvas.create_oval(self.width - radius * 2, 0, self.width, radius * 2, fill=header_bg, outline="")

        # Draw body fill (bottom part with rounded bottom corners)
        self.card_canvas.create_rectangle(0, header_height, self.width, self.height, fill=self.bg_color, outline="")
        self.card_canvas.create_oval(0, self.height - radius * 2, radius * 2, self.height, fill=self.bg_color, outline="")
        self.card_canvas.create_oval(self.width - radius * 2, self.height - radius * 2, self.width, self.height, fill=self.bg_color, outline="")

        # Draw the outline around the entire card
        self._draw_rounded_outline(
            self.card_canvas,
            0,
            0,
            self.width,
            self.height,
            radius,
            outline=card_border,
            line_width=card_border_width
        )

        if self.text:
            self.header_text_id = self.card_canvas.create_text(
                16,
                8,
                text=self.text,
                font=("Segoe UI", 13, "bold"),
                fill=header_fg,
                anchor="nw"
            )

        Misc.lift(self.card_canvas)

    def _draw_rounded_rect(self, canvas, x, y, w, h, r, fill, outline, line_width):
        # Fill
        canvas.create_rectangle(x + r, y, x + w - r, y + h, fill=fill, outline="")
        canvas.create_rectangle(x, y + r, x + w, y + h - r, fill=fill, outline="")
        canvas.create_oval(x, y, x + 2 * r, y + 2 * r, fill=fill, outline="")
        canvas.create_oval(x + w - 2 * r, y, x + w, y + 2 * r, fill=fill, outline="")
        canvas.create_oval(x, y + h - 2 * r, x + 2 * r, y + h, fill=fill, outline="")
        canvas.create_oval(x + w - 2 * r, y + h - 2 * r, x + w, y + h, fill=fill, outline="")

        # Outline
        self._draw_rounded_outline(canvas, x, y, w, h, r, outline, line_width)

    def _draw_rounded_outline(self, canvas, x, y, w, h, r, outline, line_width):
        if not outline:
            return

        # Straight lines
        canvas.create_line(x + r, y, x + w - r, y, fill=outline, width=line_width)  # Top
        canvas.create_line(x + r, y + h, x + w - r, y + h, fill=outline, width=line_width)  # Bottom
        canvas.create_line(x, y + r, x, y + h - r, fill=outline, width=line_width)  # Left
        canvas.create_line(x + w, y + r, x + w, y + h - r, fill=outline, width=line_width)  # Right

        # Corner arcs
        canvas.create_arc(x, y, x + 2 * r, y + 2 * r, start=90, extent=90, outline=outline, width=line_width, style="arc")  # Top-left
        canvas.create_arc(x + w - 2 * r, y, x + w, y + 2 * r, start=0, extent=90, outline=outline, width=line_width, style="arc")  # Top-right
        canvas.create_arc(x, y + h - 2 * r, x + 2 * r, y + h, start=180, extent=90, outline=outline, width=line_width, style="arc")  # Bottom-left
        canvas.create_arc(x + w - 2 * r, y + h - 2 * r, x + w, y + h, start=270, extent=90, outline=outline, width=line_width, style="arc")  # Bottom-right

    def set_text(self, new_text: str):
        if hasattr(self, 'header_text_id'):
            self.card_canvas.itemconfig(self.header_text_id, text=new_text)
        else:
            pass