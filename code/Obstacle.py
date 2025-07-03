#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame
from code.Entity import Entity
from abc import ABC, abstractmethod
import pygame

class Obstacle(Entity):
    def __init__(self, name, position, size=(80, 100)):
        super().__init__(name, position, size)
        self.rect.y = 310

# code/Obstacle.py
import pygame

class Obstacle:
    def __init__(self, name, position, size=(80, 100)):
        self.name = name
        self.position = position
        self.surf = pygame.image.load(f'./asset/{name}.png').convert_alpha()
        self.surf = pygame.transform.scale(self.surf, size)
        self.rect = self.surf.get_rect(topleft=position)

    def move(self):
        raise NotImplementedError("Subclasses devem implementar o método move()")
