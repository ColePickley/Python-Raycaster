class Player:
    def __init__(self, grid_x, grid_y, rotation, grid_size):
        if not isinstance(grid_x, int) or not isinstance(grid_y, int):
            raise Exception('Player grid positions must be of type integer')
        if grid_size < 8:
            raise Exception('grid_size must be at least 8')

        #centers the player's position within the specified grid space
        self.x = grid_size * grid_x + grid_size / 2
        self.y = grid_size * grid_y + grid_size / 2

        self.rotation = rotation
        self.velocity_x = 0
        self.velocity_y = 0
