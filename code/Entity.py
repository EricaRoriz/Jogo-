#!/usr/bin/python
# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
import pygame

class Entity(ABC):
    def __init__(self, name: str, position: tuple, size=(100, 100)):
        self.name = name
        self.surf = pygame.image.load('./asset/' + name + '.png')

        # Redimensiona backgrounds para o tamanho da tela 701x458
        if "Level1Bg" in name or "Level2Bg" in name or "Bg" in name:
            self.surf = pygame.transform.scale(self.surf, (701, 458))
        else:
            # Redimensiona personagens com o tamanho passado em size
            self.surf = pygame.transform.scale(self.surf, size)

        self.rect = self.surf.get_rect(left=position[0], top=position[1])
        self.speed = 0

    @abstractmethod
    def move(self):
        pass
