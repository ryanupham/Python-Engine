class Position:
    def __init__(self, x=0, y=0, x_vel=0, y_vel=0):
        self.x, self.y, self.x_vel, self.y_vel = x, y, x_vel, y_vel

    def step(self) -> None:
        self.x += self.x_vel
        self.y += self.y_vel
