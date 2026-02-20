from BirdsEyeWindow import BirdsEyeWindow
from GameWindow import GameWindow

class WindowController:
    def __init__(self, root, ray_thickness, map_grid, grid_size, player):
        self.root = root
        self.gw = GameWindow(root, ray_thickness, player)
        self.bw = BirdsEyeWindow(root, map_grid, grid_size)

    def start_windows(self, player, rays):
        self.gw.start(rays)
        self.bw.start(player, rays)
        self.root.mainloop()

    def update_windows(self, player, rays):
        self.gw.update(rays)
        self.bw.update(player, rays)