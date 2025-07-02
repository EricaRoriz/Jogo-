#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import pygame
import random
from pygame import Surface, Rect
from pygame.font import Font

from code.Player import Player
from code.Enemy import Enemy
from code.EntityFactory import EntityFactory
from code.const import C_WHITE, WIN_HEIGHT


class Level:
    def __init__(self, window, name, menu_return):
        self.window = window
        self.name = name
        self.menu_return = menu_return
        self.timeout = 60000  # 60 segundos

        # Carrega backgrounds para parallax
        self.entity_list = EntityFactory.get_entity('Level1Bg')
        self.layer_offsets = [0.0] * len(self.entity_list)
        self.layer_speeds = [0.2 + i * 0.5 for i in range(len(self.entity_list))]

        # Cria o player ajustado
        self.player = Player((100, 320), size=(100, 140))

        # Lista de inimigos ativos
        self.enemies = []

        # Tipos de zumbis
        self.enemy_types = ['Zombie1', 'Zombie2', 'Zombie3']

        # Controle de spawn aleatório
        self.spawn_timer = 0
        self.next_spawn_time = random.randint(1000, 4000)  # em milissegundos

    def run(self):
        running = True
        clock = pygame.time.Clock()

        # Música do nível
        pygame.mixer_music.stop()
        pygame.mixer_music.load('./asset/Level1.mp3')
        pygame.mixer_music.play(-1)

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            keys = pygame.key.get_pressed()
            self.player.update(keys)

            # Controle de spawn de inimigos
            self.spawn_timer += clock.get_time()
            if self.spawn_timer >= self.next_spawn_time:
                name = random.choice(self.enemy_types)
                new_enemy = Enemy(name, (701, 320), size=(70, 100))
                self.enemies.append(new_enemy)
                self.spawn_timer = 0
                self.next_spawn_time = random.randint(7000, 10000)


            # Atualiza inimigos
            for enemy in self.enemies:
                enemy.move()

            self.update()
            self.draw()

            # HUD
            self.level_text(14, f'{self.name} - Timeout: {self.timeout / 1000:.1f}s', C_WHITE, (10, 5))
            self.level_text(14, f'fps: {clock.get_fps():.0f}', C_WHITE, (10, WIN_HEIGHT - 35))
            self.level_text(14, f'entidades: {len(self.entity_list)}', C_WHITE, (10, WIN_HEIGHT - 20))

            pygame.display.flip()
            clock.tick(60)

    def level_text(self, text_size: int, text: str, text_color: tuple, text_pos: tuple):
        font = pygame.font.SysFont("Lucida Sans Typewriter", text_size)
        surf = font.render(text, True, text_color).convert_alpha()
        rect = surf.get_rect(topleft=text_pos)
        self.window.blit(surf, rect)

    def update(self):
        # Parallax update
        for i in range(len(self.entity_list)):
            self.layer_offsets[i] -= self.layer_speeds[i]
            if self.layer_offsets[i] <= -701:
                self.layer_offsets[i] = 0

    def draw(self):
        # Fundo com parallax
        for i, entity in enumerate(self.entity_list):
            offset = self.layer_offsets[i]
            self.window.blit(entity.surf, (offset, 0))
            self.window.blit(entity.surf, (offset + 701, 0))

        # Player
        self.window.blit(self.player.surf, self.player.rect)

        # Inimigos
        for enemy in self.enemies:
            self.window.blit(enemy.surf, enemy.rect)
