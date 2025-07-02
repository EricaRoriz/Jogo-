import pygame


class Bullet(pygame.sprite.Sprite):
    def __init__(self, position, flipped):
        super().__init__()
        self.image = pygame.image.load('./asset/Bullet.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect(center=position)
        self.speed = -10 if flipped else 10

    def move(self):
        self.rect.x += self.speed

    def update(self):
        self.move()
