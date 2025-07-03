# code/StaticObstacle.py
from code.Obstacle import Obstacle

class StaticObstacle(Obstacle):
    def __init__(self, name, position, size=(70, 90)):
        super().__init__(name, position, size)
        self.speed = 2  # mesma velocidade dos zumbis

    def move(self):
        self.rect.x -= self.speed

