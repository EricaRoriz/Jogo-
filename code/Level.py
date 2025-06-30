#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame.display

from code.Entity import Entity
from code.EntityFactory import EntityFactory
from typing import List
from code.Entity import Entity  # se não tiver, adicione esse import




#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
from code.EntityFactory import EntityFactory

class Level:
    def __init__(self, window, name, menu_return):
        self.window = window
        self.name = name
        self.menu_return = menu_return

        # Carrega as 9 camadas de fundo com base no nome
        self.entity_list = EntityFactory.get_entity('Level1Bg')

        # Posição X de cada layer (pra simular deslocamento)
        self.layer_offsets = [0.0] * len(self.entity_list)

        # Velocidade de deslocamento de cada camada
        self.layer_speeds = [0.2 + i * 1 for i in range(len(self.entity_list))]

    def run(self):
        running = True
        clock = pygame.time.Clock()
        pygame.mixer_music.stop()
        pygame.mixer_music.load('./asset/Level1.mp3')
        pygame.mixer_music.play(-1)
        while running:
            # EVENTS
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    quit()


            # UPDATE
            self.update()

            # DRAW
            self.draw()

            # Atualiza a tela
            pygame.display.flip()
            clock.tick(60)  # 60 FPS


    def update(self):
        for i in range(len(self.entity_list)):
            self.layer_offsets[i] -= self.layer_speeds[i]
            if self.layer_offsets[i] <= -701:
                self.layer_offsets[i] = 0

    def draw(self):
        for i, entity in enumerate(self.entity_list):
            offset = self.layer_offsets[i]
            self.window.blit(entity.surf, (offset, 0))
            self.window.blit(entity.surf, (offset + 701, 0))
