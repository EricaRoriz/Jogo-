#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame
from code.Entity import Entity

class Enemy(Entity):
    def __init__(self, name, position, size=(70, 100)):
        super().__init__(name, position)
        self.speed = 2
        self.health = 3
        self.surf = pygame.transform.scale(self.surf, size)
        self.surf = pygame.transform.flip(self.surf, True, False)

    def move(self):
        self.rect.x -= self.speed

    def hit(self):
        self.health -= 1
