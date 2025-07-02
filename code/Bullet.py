#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame
from code.Entity import Entity

class Bullet(Entity):
    def __init__(self, position, flipped, speed=10):
        super().__init__('Bullet', position, size=(20, 10))
        self.speed = -speed if flipped else speed

    def move(self):
        self.rect.x += self.speed
