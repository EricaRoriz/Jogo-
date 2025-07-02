#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame
from code.Entity import Entity

class Player(Entity):
    def __init__(self, position, size=(100, 150)):
        super().__init__('Player1', position, size)
        self.speed = 5
        self.jump_speed = -15
        self.gravity = 1
        self.velocity_y = 0
        self.on_ground = True

    def update(self, keys_pressed):
        # Movimento horizontal controlado
        if keys_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys_pressed[pygame.K_RIGHT]:
            self.rect.x += self.speed

        # Limita a posição horizontal dentro da janela (701 largura)
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 701:
            self.rect.right = 701

        # Pulo
        if keys_pressed[pygame.K_SPACE] and self.on_ground:
            self.velocity_y = self.jump_speed
            self.on_ground = False

        # Gravidade
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y

        # Colisão com o "chão" ajustado para y=320 (subiu um pouco)
        if self.rect.y >= 285:
            self.rect.y = 285
            self.on_ground = True
            self.velocity_y = 0

    def move(self):
        pass  # método abstrato implementado, pode ficar vazio
