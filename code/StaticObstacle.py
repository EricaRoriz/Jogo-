import pygame
from code.Obstacle import Obstacle


class StaticObstacle(Obstacle):
    def __init__(self, name, position, size=None, speed=5):
        if size is None:
            size = (80, 100)
        super().__init__(name, position, size)
        self.speed = speed

    def move(self):
        self.rect.x -= self.speed
