class Ray:
    def __init__(self, degree):
        self.length = 0
        self.degree = degree #is the degree from the players directional vector that the ray is cast from
        self.is_vertical_collision = False
