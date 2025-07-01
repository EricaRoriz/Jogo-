#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import pygame
from pygame import Surface, Rect
from pygame.font import Font

from code.Entity import Entity
from code.EntityFactory import EntityFactory
from code.const import C_WHITE, WIN_HEIGHT

class Level:
    def __init__(self, window, name, menu_return):
        self.window = window
        self.name = name
        self.menu_return = menu_return
        self.entity_list = EntityFactory.get_entity('Level1Bg')
        self.layer_offsets = [0.0] * len(self.entity_list)
        self.layer_speeds = [0.2 + i * 0.5 for i in range(len(self.entity_list))]
        self.timeout = 60000  # 60 segundos

    def run(self):
        running = True
        clock = pygame.time.Clock()

        pygame.mixer_music.stop()
        pygame.mixer_music.load('./asset/Level1.mp3')
        pygame.mixer_music.play(-1)

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()

            self.update()
            self.draw()

            # Exibe textos na tela
            self.level_text(14, f'{self.name} - Timeout: {self.timeout / 1000:.1f}s', C_WHITE, (10, 5))
            self.level_text(14, f'fps: {clock.get_fps():.0f}', C_WHITE, (10, WIN_HEIGHT - 35))
            self.level_text(14, f'entidades: {len(self.entity_list)}', C_WHITE, (10, WIN_HEIGHT - 20))

            pygame.display.flip()
            clock.tick(60)

    def level_text(self, text_size: int, text: str, text_color: tuple, text_pos: tuple):
        text_font: Font = pygame.font.SysFont("Lucida Sans Typewriter", text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(left=text_pos[0], top=text_pos[1])
        self.window.blit(text_surf, text_rect)

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
