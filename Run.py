from Raycaster import Raycaster
from Player import Player

"""
Welcome to my raycaster program!
If you don't know what a raycaster is, it's a 3D simulation of a 2D space.
This simulation is accomplished by sending rays out from the player's position
and detecting the length of those rays when they hit a wall. Those rays are then
translated to vertical lines on the screen.

To help users understand what's going on, I've creates a window with a birds-eye
view of the map, player, and rays along side the normal game window.

You can create maps using 2D arrays for the raycaster to process. I've left a few
examples for you to try, but feel free to make your own. The coordinates on the map
grids start at x = 0, y = 0 in the top left corner.
"""

map_grid1 = [[1, 1, 1, 1, 1, 1, 1, 1, 1],
             [1, 0, 1, 0, 0, 0, 1, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 1, 1, 0, 1, 1, 0, 1],
             [1, 0, 1, 0, 0, 0, 1, 0, 1],
             [1, 0, 1, 1, 0, 1, 1, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 1, 0, 0, 0, 1, 0, 1],
             [1, 1, 1, 1, 1, 1, 1, 1, 1]]

map_grid2 = [[1, 1, 1, 1, 1, 1, 1, 1, 1],
             [1, 0, 1, 0, 0, 0, 1, 0, 1],
             [1, 0, 0, 0, 1, 0, 0, 0, 1],
             [1, 1, 1, 1, 1, 1, 1, 1, 1]]

player_grid_x = 1 #x coordinate for the grid space you want the player to start in
player_grid_y = 3 #y coordinate for the grid space you want the player to start in
player_rotation = 0 #player's starting rotation in degrees with 0 being directly down
grid_size = 64 #arbitrary number affecting how large the grid spaces appear to the player

player = Player(player_grid_x, player_grid_y, player_rotation, grid_size)
raycaster = Raycaster(map_grid1, grid_size, player)
raycaster.start()