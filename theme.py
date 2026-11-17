import os
import sys
import time
import tkinter as tk
from tkinter import font, ttk

BG = "#0f1117"
SURFACE = "#181b24"
SURFACE_ALT = "#1f2330"
BORDER = "#2a2f3d"

TEXT = "#e8eaf0"
MUTED = "#8b93a7"

ACCENT = "#6c8cff"
ACCENT_HOVER = "#8aa3ff"
ACCENT_TEXT = "#0b0e16"

WAIT = "#e5484d"
GO = "#30a46c"
EARLY = "#3e63dd"
RESULT = "#2b3040"
CIRCLE = "#30a46c"
CIRCLE_OUTLINE = "#7ee2a8"

GAME_BG = "#121417"
GRID = "#1C2026"
GRID_SIZE = 40

HIT = "#3dff8a"
MISS = "#ff4d4d"
SHADOW = "#000000"
WHITE = "#ffffff"




CROSSHAIR_COLORS = {"Blue": "#00e5ff", "Green": "#39ff14", "Purple": "#ff2bd6"}
CROSSHAIR_STYLES = ("Cross", "Dot", "Circle")
settings = {"color": "Blue", "style": "Cross"}

FONT = "Helvetica"
DISPLAY_FONT = "Orbitron"
FONT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")

if sys.platform == "win32":
    import ctypes
    for file_name in os.listdir(FONT_DIR):
        if file_name.endswith(".ttf"):
            ctypes.windll.gdi32.AddFontResourceExW(os.path.join(FONT_DIR, file_name), 0x10, 0)




def display_font():
    return DISPLAY_FONT if DISPLAY_FONT in font.families() else FONT




def blend(color_a, color_b, amount):
    a = [int(color_a[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(color_b[i:i + 2], 16) for i in (1, 3, 5)]
    return "#%02x%02x%02x" % tuple(round(a[i] + (b[i] - a[i]) * amount) for i in range(3))


def draw_crosshair(canvas, x, y, color=None):
    canvas.delete("crosshair")
    color = color or CROSSHAIR_COLORS[settings["color"]]
    style = settings["style"]
    for ink, width, pad in ((SHADOW, 5, 1.5), (color, 2, 0)):
        if style == "Cross":
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                canvas.create_line(x + dx * 5, y + dy * 5, x + dx * 16, y + dy * 16,
                                   fill=ink, width=width, capstyle="round", tags="crosshair")
            radius = 1.5 + pad
        elif style == "Dot":
            radius = 3.5 + pad
        else:
            canvas.create_oval(x - 11, y - 11, x + 11, y + 11,
                               outline=ink, width=width, tags="crosshair")
            radius = 2 + pad
        canvas.create_oval(x - radius, y - radius, x + radius, y + radius,
                           fill=ink, outline=ink, tags="crosshair")


def apply_theme(root):
    root.configure(bg=BG)
    style = ttk.Style(root)
    style.theme_use("clam")
    style.configure(".", background=BG, foreground=TEXT,
                    font=(FONT, 11), bordercolor=BORDER,
                    focuscolor=BG)
    style.configure("Card.TFrame", background=SURFACE,
                    bordercolor=BORDER, borderwidth=1, relief="solid")
    style.configure("CardInner.TFrame", background=SURFACE)
    display = display_font()
    style.configure("MenuTitle.TLabel", font=(display, 28, "bold"))
    style.configure("MenuSubtitle.TLabel", foreground=MUTED, font=(display, 9))
    style.configure("MenuCardHeading.TLabel", background=SURFACE,
                    foreground=ACCENT, font=(display, 11, "bold"))
    style.configure("Title.TLabel", font=(FONT, 34, "bold"))
    style.configure("Heading.TLabel", font=(FONT, 24, "bold"))
    style.configure("Subtitle.TLabel", foreground=MUTED, font=(FONT, 12))
    style.configure("Info.TLabel", foreground=MUTED, font=(FONT, 12, "bold"))
    style.configure("Card.TLabel", background=SURFACE, font=(FONT, 11))
    style.configure("CardHeading.TLabel", background=SURFACE,
                    foreground=ACCENT, font=(FONT, 14, "bold"))
    style.configure("CardTitle.TLabel", background=SURFACE,
                    font=(FONT, 20, "bold"))
    style.configure("Stat.TLabel", background=SURFACE, font=(FONT, 14, "bold"))
    style.configure("CardMuted.TLabel", background=SURFACE,
                    foreground=MUTED, font=(FONT, 10))
    style.configure("TButton", background=SURFACE_ALT, foreground=TEXT,
                    bordercolor=BORDER, lightcolor=SURFACE_ALT,
                    darkcolor=SURFACE_ALT, relief="flat",
                    padding=(18, 10), font=(FONT, 11))
    style.map("TButton", background=[("active", BORDER)],
              bordercolor=[("active", ACCENT)])
    style.configure("Accent.TButton", background=ACCENT, foreground=ACCENT_TEXT,
                    bordercolor=ACCENT, lightcolor=ACCENT,
                    darkcolor=ACCENT, font=(FONT, 11, "bold"))
    style.map("Accent.TButton", background=[("active", ACCENT_HOVER)],
              bordercolor=[("active", ACCENT_HOVER)])
    style.configure("Menu.TButton", font=(display, 10, "bold"))
    style.map("Menu.TButton", background=[("active", BORDER)],
              bordercolor=[("active", ACCENT)])
    style.configure("MenuAccent.TButton", background=ACCENT, foreground=ACCENT_TEXT,
                    bordercolor=ACCENT, lightcolor=ACCENT,
                    darkcolor=ACCENT, font=(display, 10, "bold"))
    style.map("MenuAccent.TButton", background=[("active", ACCENT_HOVER)],
              bordercolor=[("active", ACCENT_HOVER)])


class Effects:
    def setup_effects(self):
        self.effect_jobs = set()
        self.pointer = None
        self.crosshair_color = None
        self.canvas.configure(bg=BG, cursor="none")
        self.canvas.bind("<Motion>", self.move_pointer)
        self.canvas.bind("<Enter>", self.move_pointer)
        self.canvas.bind("<Leave>", self.hide_pointer)



    def draw_panel(self, width, height, color):
        self.canvas.delete("scene")
        r = max(1, min(28, width // 4, height // 4))
        x1, y1, x2, y2 = 2, 2, width - 2, height - 2
        outline = GRID if color == GAME_BG else color
        self.canvas.create_polygon(
            x1 + r, y1, x2 - r, y1, x2, y1, x2, y1 + r, x2, y2 - r, x2, y2,
            x2 - r, y2, x1 + r, y2, x1, y2, x1, y2 - r, x1, y1 + r, x1, y1,
            smooth=True, fill=color, outline=outline, tags="scene")
        if color == GAME_BG:
            for gx in range(x1 + GRID_SIZE, x2, GRID_SIZE):
                self.canvas.create_line(gx, y1, gx, y2, fill=GRID, tags="scene")
            for gy in range(y1 + GRID_SIZE, y2, GRID_SIZE):
                self.canvas.create_line(x1, gy, x2, gy, fill=GRID, tags="scene")

    def finish_draw(self):
        self.canvas.tag_raise("fx")
        if self.pointer is not None:
            draw_crosshair(self.canvas, *self.pointer, self.crosshair_color)

    def draw_extras(self):
        pass

    def move_pointer(self, event):
        self.pointer = (event.x, event.y)
        draw_crosshair(self.canvas, event.x, event.y, self.crosshair_color)

    def hide_pointer(self, event=None):
        self.pointer = None
        self.canvas.delete("crosshair")

    def animate(self, duration_ms, update, finish=None):
        start = time.perf_counter()
        state = {"job": None}

        def frame():
            self.effect_jobs.discard(state["job"])
            progress = min(1.0, (time.perf_counter() - start) * 1000 / duration_ms)
            update(progress)
            if progress < 1.0:
                state["job"] = self.after(16, frame)
                self.effect_jobs.add(state["job"])
            elif finish is not None:
                finish()

        frame()



    def cancel_effects(self):
        for job in list(self.effect_jobs):
            self.after_cancel(job)
        self.effect_jobs.clear()
        self.crosshair_color = None
        try:
            self.canvas.delete("fx")
        except tk.TclError:
            pass

    def spawn_ring(self, x, y, color, start_radius=6, end_radius=34, duration_ms=160):
        ring = self.canvas.create_oval(x, y, x, y, outline=color, width=3, tags="fx")

        def update(progress):
            radius = start_radius + (end_radius - start_radius) * progress
            self.canvas.coords(ring, x - radius, y - radius, x + radius, y + radius)
            self.canvas.itemconfig(ring, width=max(1, round(3 * (1 - progress))),
                                   outline=blend(color, self.message[0], progress))



        self.animate(duration_ms, update, lambda: self.canvas.delete(ring))

    def spawn_marker(self, x, y, size=8, duration_ms=180):
        arms = [self.canvas.create_line(x - size, y - size, x + size, y + size,
                                        fill=WHITE, width=3, capstyle="round", tags="fx"),
                self.canvas.create_line(x - size, y + size, x + size, y - size,
                                        fill=WHITE, width=3, capstyle="round", tags="fx")]

        def update(progress):
            for arm in arms:
                self.canvas.itemconfig(arm, fill=blend(WHITE, self.message[0], progress ** 3))

        self.animate(duration_ms, update, lambda: [self.canvas.delete(arm) for arm in arms])

    def spawn_popup(self, x, y, text, color, duration_ms=700):
        x = min(max(x, 60), max(60, self.canvas.winfo_width() - 60))
        y = max(y, 44)
        font = (FONT, 20, "bold")
        shadow = self.canvas.create_text(x + 2, y + 2, text=text, fill=SHADOW,
                                         font=font, tags="fx")
        label = self.canvas.create_text(x, y, text=text, fill=color, font=font, tags="fx")

        def update(progress):
            lift = 54 * (1 - (1 - progress) ** 2)
            fade = max(0.0, (progress - 0.45) / 0.55)
            background = self.message[0]
            self.canvas.coords(shadow, x + 2, y + 2 - lift)
            self.canvas.coords(label, x, y - lift)
            self.canvas.itemconfig(shadow, fill=blend(SHADOW, background, fade))
            self.canvas.itemconfig(label, fill=blend(color, background, fade))



        self.animate(duration_ms, update,
                     lambda: (self.canvas.delete(shadow), self.canvas.delete(label)))

    def flash_crosshair(self, color, duration_ms=220):
        self.crosshair_color = color
        if self.pointer is not None:
            draw_crosshair(self.canvas, *self.pointer, color)

        def restore():
            if self.crosshair_color == color:
                self.crosshair_color = None
                if self.pointer is not None:
                    draw_crosshair(self.canvas, *self.pointer)

        self.animate(duration_ms, lambda progress: None, restore)

    def click_effect(self, x, y, text, color):
        self.flash_crosshair(color)
        self.spawn_ring(x, y, color)
        self.spawn_marker(x, y)
        self.spawn_popup(x, y - 22, text, color)


class CrosshairPicker(ttk.Frame):
    def __init__(self, container):
        super().__init__(container, style="Card.TFrame", padding=(16, 12))
        self.preview = tk.Canvas(self, width=64, height=64, bg=SURFACE_ALT, highlightthickness=0)
        self.preview.pack(side="left", padx=(0, 16))
        controls = ttk.Frame(self, style="CardInner.TFrame")
        controls.pack(side="left")
        ttk.Label(controls, text="Crosshair", style="MenuCardHeading.TLabel").pack(anchor="w", pady=(0, 6))
        self.color_button = ttk.Button(controls, style="Menu.TButton", width=18, cursor="hand2",
                                       command=self.cycle_color)
        self.color_button.pack(pady=3)
        self.style_button = ttk.Button(controls, style="Menu.TButton", width=18, cursor="hand2",
                                       command=self.cycle_style)
        self.style_button.pack(pady=3)
        self.refresh()

    def refresh(self):
        self.color_button["text"] = f"Color: {settings['color']}"
        self.style_button["text"] = f"Style: {settings['style']}"
        draw_crosshair(self.preview, 32, 32)

    def cycle_color(self):
        names = list(CROSSHAIR_COLORS)
        settings["color"] = names[(names.index(settings["color"]) + 1) % len(names)]
        self.refresh()

    def cycle_style(self):
        settings["style"] = CROSSHAIR_STYLES[(CROSSHAIR_STYLES.index(settings["style"]) + 1)
                                             % len(CROSSHAIR_STYLES)]
        self.refresh()
