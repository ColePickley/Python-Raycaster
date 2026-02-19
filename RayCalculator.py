import math

class RayCalculator:
    def __init__(self, map_grid, grid_size):
        self.map_grid = map_grid
        self.grid_size = grid_size
        self.gridx, self.gridy = None, None #grid location current end of the ray exists in
        self.x, self.y = None, None #coordinates on the current end of the ray
        self.rad = None #rotation of the ray in radians
        self.orientation = None #this is an integer value assigned using self.rad to help with simplifying the code

        """
        Each ray has two potential lengths which are calculated with the grid and ray deltas.
        The two ray lengths are then compared to determine which one is correct. Finally, that
        information is stored in the final deltas and length variables.
        """
        self.length1, self.length2 = None, None
        self.grid_deltax, self.grid_deltay = None, None
        self.ray_deltax, self.ray_deltay = None, None
        self.final_deltax, self.final_deltay = None, None
        self.final_length = None

    #Sets the length of all the Ray objects
    #This is the primary function of the RayCalculator class
    def set_ray_lengths(self, player, rays):
        for ray in rays:
            length = 0
            #resets variables for the new Ray
            self.set_coords(player.x, player.y)
            self.set_rad(player.rotation, ray.degree)
            self.set_orientation()
            self.set_grid_coords()

            #this loop checks one grid space at a time for a wall collision
            collision = False
            while not collision:
                self.cycle_vars()
                self.set_vertical_collision(ray)
                self.set_grid_coords()
                if self.map_grid[self.gridy][self.gridx] == 1:
                    collision = True
                length += self.final_length
            ray.length = length
        return

    #calculates ray properties for the next grid space
    def cycle_vars(self):
        self.set_grid_deltas()
        self.set_ray_deltas()
        self.set_lengths()
        self.set_final_deltas()
        self.move_coords()

    def set_coords(self, x, y):
        self.x = x
        self.y = y

    def move_coords(self):
        self.x += self.final_deltax
        self.y += self.final_deltay

    def set_rad(self, pr, deg):
        self.rad = math.radians(deg + pr)
        if self.rad < 0:
            self.rad += 2 * math.pi
        elif self.rad >= 2 * math.pi:
            self.rad -= 2 * math.pi

    def set_orientation(self):
        if self.rad == 0:
            self.orientation = 0
        elif self.rad < math.pi / 2:
            self.orientation = 1
        elif self.rad == math.pi / 2:
            self.orientation = 2
        elif self.rad < math.pi:
            self.orientation = 3
        elif self.rad == math.pi:
            self.orientation = 4
        elif self.rad < 3 * math.pi / 2:
            self.orientation = 5
        elif self.rad == 3 * math.pi / 2:
            self.orientation = 6
        else:
            self.orientation = 7

    def set_grid_deltas(self):
        if self.orientation == 0 or self.orientation == 4:
            self.grid_deltax = 0
        elif self.orientation < 4:
            self.grid_deltax = self.grid_size - (self.x % self.grid_size)
        elif self.x % self.grid_size == 0:
            self.grid_deltax = -self.grid_size
        else:
            self.grid_deltax = -1 * (self.x % self.grid_size)

        if self.orientation == 2 or self.orientation == 6:
            self.grid_deltay = 0
        elif self.orientation < 2 or self.orientation > 6:
            self.grid_deltay = self.grid_size - (self.y % self.grid_size)
        elif self.y % self.grid_size == 0:
            self.grid_deltay = -self.grid_size
        else:
            self.grid_deltay = -1 * (self.y % self.grid_size)

    def set_ray_deltas(self):
        match self.orientation:
            case 0 | 4:
                self.ray_deltax = 0
                self.ray_deltay = self.grid_deltay
            case 2 | 6:
                self.ray_deltax = self.grid_deltax
                self.ray_deltay = 0
            case 1 | 5:
                self.ray_deltax = math.tan(self.rad) * self.grid_deltay
                self.ray_deltay = self.grid_deltax / math.tan(self.rad)
            case 3 | 7:
                self.ray_deltax = -1 * self.grid_deltay / math.tan(self.rad - math.pi / 2)
                self.ray_deltay = -1 * math.tan(self.rad - math.pi / 2) * self.grid_deltax

    def set_lengths(self):
        self.length1 = (self.ray_deltax ** 2 + self.grid_deltay ** 2) ** (1 / 2)
        self.length2 = (self.ray_deltay ** 2 + self.grid_deltax ** 2) ** (1 / 2)

    def set_final_deltas(self):
        if self.length1 == self.length2:
            self.final_deltax = self.grid_deltax
            self.final_deltay = self.grid_deltay
            self.final_length = self.length1
        elif self.length1 > self.length2:
            self.final_deltax = self.grid_deltax
            self.final_deltay = self.ray_deltay
            self.final_length = self.length2
        else:
            self.final_deltax = self.ray_deltax
            self.final_deltay = self.grid_deltay
            self.final_length = self.length1

    def set_grid_coords(self):
        if 4 < self.orientation and self.x % self.grid_size == 0:
            self.gridx = int(self.x / self.grid_size) - 1
        else:
            self.gridx = int(self.x / self.grid_size)

        if 2 < self.orientation < 6 and self.y % self.grid_size == 0:
            self.gridy = int(self.y / self.grid_size) - 1
        else:
            self.gridy = int(self.y / self.grid_size)

    """
    Tells the ray object if it's collision was on a vertical grid line.
    This information determines the color that the ray will be drawn with in the GameWindow.
    """
    def set_vertical_collision(self, ray):
        if self.orientation == 2 or self.orientation == 6:
            ray.is_vertical_collision = True
        elif self.orientation == 0 or self.orientation == 4:
            ray.is_vertical_collision = False
        elif self.length1 > self.length2:
            ray.is_vertical_collision = True
        else:

            ray.is_vertical_collision = False

