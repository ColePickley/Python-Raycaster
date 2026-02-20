import tkinter as tk
import math

class GameWindow:
    def __init__(self, root, ray_thickness, player):
        self.root = root
        self.root.title('Game')
        self.canvas_width = 361 * ray_thickness # (num rays * ray thickness)
        self.canvas_height = 512  # arbitrary height
        self.canvas = tk.Canvas(self.root, width=self.canvas_width, height=self.canvas_height, bg="white",
                                highlightthickness=0, borderwidth=0)
        self.canvas.pack(padx=5, pady=5)

        self.player = player
        self.ray_thickness = ray_thickness
        self.ray_lengths = []

        self.root.bind('<Button-1>', self.on_drag_start)
        self.root.bind('<B1-Motion>', self.on_drag_motion)
        self.root.bind('<ButtonRelease-1>', self.on_drag_release)
        self.root.bind('<KeyPress>', self.on_key_press)
        self.root.bind('<KeyRelease>', self.on_key_release)
        self.drag_data = {"x": 0, "item": None}  # tracks mouse drag data

    def start(self, rays):
        self.set_ray_lengths(rays)
        self.draw_rays(rays)

    def draw_rays(self, rays):
        for i in range(len(rays)):
            color = '#0000FF'
            if rays[i].is_vertical_collision:
                color = '#0000D0'
            self.canvas.create_rectangle(self.ray_thickness * i,
                                         (self.canvas_height - self.ray_lengths[i]) / 2,
                                         (i + 1) * self.ray_thickness,
                                         (self.canvas_height + self.ray_lengths[i]) / 2,
                                         fill=color, width=0)

    def update(self, rays):
        self.set_ray_lengths(rays)
        self.canvas.delete("all")
        self.draw_rays(rays)

    """
    The length attribute stored in each Ray object is not the length of the rays seen in the
    game window. First those initial ray lengths need to be displayed, they first need to be
    converted.
    """
    def set_ray_lengths(self, rays):
        self.ray_lengths = []
        for ray in rays:
            self.ray_lengths.append(64 * self.canvas_height / (ray.length * math.cos(math.radians(ray.degree))))

    # detects mouse x at the beginning of a drag
    def on_drag_start(self, event):
        current_item = self.canvas.find_closest(event.x, event.y)[0]
        self.drag_data["item"] = current_item
        self.drag_data["x"] = event.x

    # detects the amount the mouse has been dragged and changed the players rotation
    def on_drag_motion(self, event):
        delta_x = event.x - self.drag_data["x"]
        self.player.rotation += delta_x
        self.drag_data["x"] = event.x

    #detetcts when a mouse drag is over
    def on_drag_release(self, event):
        self.drag_data["item"] = None
        self.drag_data["x"] = 0

    #detects when movement keys are pressed and sets the player's directional velocities
    def on_key_press(self, event):
        speed = 3
        rot1 = math.radians(self.player.rotation)
        rot2 = math.radians(self.player.rotation + 90)
        match event.char:
            case 'w':
                self.player.velocity_x = speed * math.sin(rot1)
                self.player.velocity_y = speed * math.cos(rot1)
            case 'a':
                self.player.velocity_x = -speed * math.sin(rot2)
                self.player.velocity_y = -speed * math.cos(rot2)
            case 's':
                self.player.velocity_x = -speed * math.sin(rot1)
                self.player.velocity_y = -speed * math.cos(rot1)
            case 'd':
                self.player.velocity_x = speed * math.sin(rot2)
                self.player.velocity_y = speed * math.cos(rot2)

    # detects when movement keys are lifted and sets the player's directional velocities to 0
    def on_key_release(self, event):
        if event.char == 'w' or event.char == 'a' or event.char == 's' or event.char == 'd':
            self.player.velocity_x = 0
            self.player.velocity_y = 0