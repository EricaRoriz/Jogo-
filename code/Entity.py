#!/usr/bin/python
# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod

import pygame


class Entity(ABC):
    def __init__(self, name: str, position: tuple):
        self.name = name
        image_path = './asset/' + name + '.png'
        self.surf = pygame.image.load(image_path)

        # Verifica se é um background (pode usar prefixo ou nome completo)
        if "Level1Bg" in name or "Level2Bg" in name or "Bg" in name:
            self.surf = pygame.transform.scale(self.surf, (701, 458))

        self.rect = self.surf.get_rect(left=position[0], top=position[1])
        self.speed = 0


    @abstractmethod
    def move(self, ):
        pass
