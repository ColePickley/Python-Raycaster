import tkinter as tk
import math

class BirdsEyeWindow:
    def __init__(self, root, map_grid, grid_size):
        self.map_grid = map_grid
        self.grid_size = grid_size
        self.canvas_width = self.grid_size * len(map_grid[0])
        self.canvas_height = self.grid_size * len(map_grid)
        self.window = tk.Toplevel(root)
        self.window.title('BirdsEye')
        self.canvas = tk.Canvas(self.window, width=self.canvas_width, height=self.canvas_height, bg="gray",
                                highlightthickness=0, borderwidth=0)
        self.canvas.pack(padx=5, pady=5)
        self.player = None
        self.ray_lines = [None] * 361

    def start(self, player, rays):
        self.draw_map()
        self.draw_rays(player, rays)
        self.player = self.canvas.create_oval(player.x - 2, player.y - 2, player.x + 2, player.y + 2, fill="red",
                                              outline="black", width=0)

    def draw_map(self):
        counter = 0
        for row in self.map_grid:
            for cell in row:
                x = self.grid_size * (counter % len(self.map_grid[0]))
                y = int(counter / len(self.map_grid[0])) * self.grid_size
                if cell == 1:
                    self.canvas.create_rectangle(x, y, x + self.grid_size, y + self.grid_size, fill="blue",
                                                 outline="black", width=2)
                else:
                    self.canvas.create_rectangle(x, y, x + self.grid_size, y + self.grid_size, fill="white",
                                                 outline="black", width=2)
                counter += 1

    def draw_rays(self, player, rays):
        pr = math.radians(player.rotation)
        i = -45
        for j in range(0, 360):
            rad = math.radians(i)
            self.ray_lines[j] = self.canvas.create_line(player.x, player.y,
                                                        rays[j].length * math.sin(rad + pr) + player.x,
                                                        rays[j].length * math.cos(rad + pr) + player.y,
                                                        fill="red", width=1)
            i += 0.25

    def update(self, player, rays):
        self.canvas.delete(self.player)
        for ray_line in self.ray_lines:
            self.canvas.delete(ray_line)
        self.player = self.canvas.create_oval(player.x - 2, player.y - 2, player.x + 2, player.y + 2, fill="red",
                                              outline="black", width=0)
        self.draw_rays(player, rays)