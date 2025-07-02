#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import pygame
import random

from code.Bullet import Bullet
from code.Player import Player
from code.Enemy import Enemy
from code.StaticObstacle import StaticObstacle
from code.EntityFactory import EntityFactory
from code.const import C_WHITE, WIN_HEIGHT


class Level:
    def __init__(self, window, name, menu_return):
        self.window = window
        self.name = name
        self.menu_return = menu_return
        self.timeout = 60000  # 60 segundos
        self.last_spawned_type = None

        self.bullets = pygame.sprite.Group()
        self.shoot_sound = pygame.mixer.Sound('./asset/gunshot.wav')

        # Backgrounds com parallax
        self.entity_list = EntityFactory.get_entity('Level1Bg')
        self.layer_offsets = [0.0] * len(self.entity_list)
        self.layer_speeds = [0.2 + i * 0.5 for i in range(len(self.entity_list))]

        # Player
        self.player = Player((100, 320), size=(100, 140))

        # Tipos de entidades
        self.enemy_types = ['Zombie1', 'Zombie2', 'Zombie3']
        self.obstacle_types = ['Hand', 'Lapide', 'Bones']
        self.entities = []

        # Timer de spawn
        self.spawn_timer = 0
        self.next_spawn_time = random.randint(1000, 4000)

    def run(self):
        running = True
        clock = pygame.time.Clock()

        pygame.mixer_music.stop()
        pygame.mixer_music.load('./asset/Level1.mp3')
        pygame.mixer_music.play(-1)

        while running:
            # --- Eventos de teclado ---
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        bullet = self.player.shoot()
                        self.bullets.add(bullet)
                        pygame.mixer.Sound.play(self.shoot_sound)

            # --- Atualização do jogador ---
            keys = pygame.key.get_pressed()
            self.player.update(keys)

            # --- Atualização das balas ---
            self.bullets.update()
            for bullet in self.bullets.copy():
                if bullet.rect.right < 0 or bullet.rect.left > 701:
                    self.bullets.remove(bullet)
                    continue

                # Verifica colisão com zumbis
                for entity in self.entities[:]:
                    if isinstance(entity, Enemy) and entity.rect.colliderect(bullet.rect):
                        entity.hit()
                        if entity.health <= 0:
                            self.entities.remove(entity)
                        self.bullets.remove(bullet)
                        break

            # --- Spawning de inimigos e obstáculos ---
            self.spawn_timer += clock.get_time()
            if self.spawn_timer >= self.next_spawn_time:
                spawn_type = random.choice(['enemy', 'obstacle'])
                if self.last_spawned_type == 'obstacle' and spawn_type == 'obstacle':
                    spawn_type = 'enemy'

                if spawn_type == 'enemy':
                    name = random.choice(self.enemy_types)
                    new_entity = Enemy(name, (701, 320), size=(70, 100))
                    self.last_spawned_type = 'enemy'
                else:
                    name = random.choice(self.obstacle_types)
                    new_entity = StaticObstacle(name, (701, 0), size=(80, 120))
                    new_entity.rect.bottom = 440 if name == 'Bones' else 430
                    self.last_spawned_type = 'obstacle'

                self.entities.append(new_entity)
                self.spawn_timer = 0
                self.next_spawn_time = random.randint(1500, 5000)

            # --- Atualiza entidades (move inimigos/obstáculos) ---
            for entity in self.entities[:]:
                entity.move()
                if entity.rect.right < 0:
                    self.entities.remove(entity)

            # --- Atualizações gerais ---
            self.update()
            self.draw()

            # --- HUD ---
            self.level_text(14, f'{self.name} - Timeout: {self.timeout / 1000:.1f}s', C_WHITE, (10, 5))
            self.level_text(14, f'fps: {clock.get_fps():.0f}', C_WHITE, (10, WIN_HEIGHT - 35))
            self.level_text(14, f'entidades: {len(self.entities)}', C_WHITE, (10, WIN_HEIGHT - 20))

            pygame.display.flip()
            clock.tick(60)

    def level_text(self, text_size: int, text: str, text_color: tuple, text_pos: tuple):
        font = pygame.font.SysFont("Lucida Sans Typewriter", text_size)
        surf = font.render(text, True, text_color).convert_alpha()
        rect = surf.get_rect(topleft=text_pos)
        self.window.blit(surf, rect)

    def update(self):
        for i, entity in enumerate(self.entity_list):
            self.layer_offsets[i] -= self.layer_speeds[i]
            width = entity.surf.get_width()
            if self.layer_offsets[i] <= -width:
                self.layer_offsets[i] = 0


    def draw(self):
        # Fundo com parallax
        for i, entity in enumerate(self.entity_list):
            offset = self.layer_offsets[i]
            width = entity.surf.get_width()
            self.window.blit(entity.surf, (offset, 0))
            self.window.blit(entity.surf, (offset + width, 0))

        # Player
        self.window.blit(self.player.surf, self.player.rect)

        # Inimigos e obstáculos
        for entity in self.entities:
            self.window.blit(entity.surf, entity.rect)

        # Balas
        self.bullets.draw(self.window)
