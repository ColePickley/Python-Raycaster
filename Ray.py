class Ray:
    def __init__(self, degree):
        self.length = 0
        self.degree = degree #the degree from the player's directional vector that the ray is cast from
        self.is_vertical_collision = False
