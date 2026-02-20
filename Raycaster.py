from WindowController import WindowController
from Ray import Ray
from RayCalculator import RayCalculator
from Player import Player
import tkinter as tk

class Raycaster:
    def __init__(self, map_grid, grid_size, player):
        if not isinstance(map_grid, list) or not all(isinstance(row, list) for row in map_grid):
            raise Exception('map_grid must be a 2D array')
        for row in map_grid:
            for cell in row:
                if not isinstance(cell, int) or cell < 0 or cell > 1:
                    raise Exception('map_grid must only contain integers between 0 and 1')
        if map_grid is None or len(map_grid) < 4 or len(map_grid[0]) < 4:
            raise Exception('map_grid is not at least a 3x3')
        for y in range(len(map_grid)):
            if map_grid[y][0] == 0 or map_grid[y][len(map_grid[0]) - 1] == 0:
                raise Exception('Map is not enclosed')
        for x in range(len(map_grid[0])):
            if map_grid[0][x] == 0 or map_grid[len(map_grid) - 1][x] == 0:
                raise Exception('Map is not enclosed')
        if not isinstance(grid_size, int):
            raise Exception('grid_size must be of type integer')
        if not isinstance(player, Player):
            raise Exception('player must be of type Player')
        if grid_size < 8:
            raise Exception('grid_size must be at least 8')

        self.map_grid = map_grid #2D array containing the map layout
        self.grid_size = grid_size #size of grid squares
        self.player = player
        self.root = tk.Tk()
        self.ray_thickness = 3 #pixel width of rays in GameWindow
        self.rays = [] #array of Ray objects
        self.rc = RayCalculator(self.map_grid, self.grid_size)
        self.window_controller = None

    #Starts the Raycaster
    def start(self):
        if len(self.map_grid[0]) * self.grid_size < self.player.x or self.player.x < 0:
            raise Exception('Player position is outside the map')
        if len(self.map_grid) * self.grid_size < self.player.y or self.player.x < 0:
            raise Exception('Player position is outside the map')
        if self.map_grid[int(self.player.y / self.grid_size)][int(self.player.x / self.grid_size)] == 1:
            raise Exception('Player position is within a wall')

        #creates the Ray objects
        i = -45.0
        while i <= 45:
            self.rays.append(Ray(i))
            i += 0.25
        self.rc.set_ray_lengths(self.player, self.rays)

        #creates windows
        self.window_controller = WindowController(self.root, self.ray_thickness, self.map_grid, self.grid_size,
                                                  self.player)
        self.update_windows()
        self.window_controller.start_windows(self.player, self.rays)

    #checks for collision and moves the player
    def move_player(self):
        if not self.is_x_collision():
            self.player.x += self.player.velocity_x
        if not self.is_y_collision():
            self.player.y += self.player.velocity_y

    #checks for a collision in the x direction
    def is_x_collision(self):
        player_grid_y = int(self.player.y / self.grid_size)
        player_grid_x = int((self.player.x + self.player.velocity_x) / self.grid_size)
        if self.map_grid[player_grid_y][player_grid_x] == 1:
            return True
        return False

    #checks for a collision in the y direction
    def is_y_collision(self):
        player_grid_y = int((self.player.y + self.player.velocity_y) / self.grid_size)
        player_grid_x = int(self.player.x / self.grid_size)
        if self.map_grid[player_grid_y][player_grid_x] == 1:
            return True
        return False

    #main game loop
    def update_windows(self):
        self.move_player()
        self.rc.set_ray_lengths(self.player, self.rays)
        self.window_controller.update_windows(self.player, self.rays)
        self.root.after(16, self.update_windows)