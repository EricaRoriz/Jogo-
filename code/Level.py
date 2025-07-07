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
        self.time_left = 5000  # 60 segundos
        self.score = 0
        self.last_spawned_type = None

        self.font = pygame.font.SysFont("Lucida Sans Typewriter", 14)

        self.bullets = pygame.sprite.Group()
        self.shoot_sound = pygame.mixer.Sound('./asset/gunshot.wav')

        self.entity_list = EntityFactory.get_entity('Level1Bg')
        self.layer_offsets = [0.0] * len(self.entity_list)
        self.layer_speeds = [0.2 + i * 1.5 for i in range(len(self.entity_list))]

        self.player = Player((100, 290), size=(85, 125))

        self.enemy_types = ['Zombie1', 'Zombie2', 'Zombie3']
        self.obstacle_types = ['Hand', 'Lapide', 'Bones']
        self.entities = []

        self.spawn_timer = 0
        self.next_spawn_time = random.randint(1000, 4000)

    def update_player(self):
        keys = pygame.key.get_pressed()
        if self.player.is_alive:
            self.player.update(keys)

    def update_bullets(self):
        self.bullets.update()
        self.bullets.draw(self.window)

        for bullet in self.bullets.copy():
            if bullet.rect.right < 0 or bullet.rect.left > 701:
                self.bullets.remove(bullet)
                continue

            for entity in self.entities[:]:
                if isinstance(entity, Enemy) and entity.rect.colliderect(bullet.rect):
                    entity.hit()
                    if entity.health <= 0:
                        self.entities.remove(entity)
                        self.score += 10
                    self.bullets.remove(bullet)
                    break

    def spawn_entities(self):
        if self.spawn_timer >= self.next_spawn_time:
            spawn_type = random.choice(['enemy', 'obstacle'])
            if self.last_spawned_type == 'obstacle' and spawn_type == 'obstacle':
                spawn_type = 'enemy'

            if spawn_type == 'enemy':
                name = random.choice(self.enemy_types)
                new_entity = Enemy(name, (701, 320), size=(70, 100))
                new_entity.rect.bottom = 420
            else:
                name = random.choice(self.obstacle_types)
                # Usar self.name para verificar o nível
                if self.name == "LEVEL 2":
                    if name == 'Bones':
                        new_entity = StaticObstacle(name, (701, 0), size=(80, 90))
                        new_entity.rect.bottom = 420
                    else:
                        new_entity = StaticObstacle(name, (701, 0), size=(70, 90))
                        new_entity.rect.bottom = 425
                else:
                    if name == 'Bones':
                        new_entity = StaticObstacle(name, (701, 0), size=(70, 70))
                        new_entity.rect.bottom = 430
                    else:
                        new_entity = StaticObstacle(name, (701, 0), size=(80, 100))
                        new_entity.rect.bottom = 420

            self.entities.append(new_entity)
            self.spawn_timer = 0
            self.next_spawn_time = random.randint(1500, 5000)
            self.last_spawned_type = spawn_type

    def move_entities(self):
        for entity in self.entities[:]:
            entity.move()
            if entity.rect.right < 0:
                self.entities.remove(entity)

    def check_collisions(self):
        if self.player.is_alive:
            for entity in self.entities:
                if self.player.rect.colliderect(entity.rect):
                    self.player.hit(damage=1)
                    if self.player.rect.left < entity.rect.left:
                        self.player.rect.x -= 10
                    else:
                        self.player.rect.x += 10
                    break

    def update_score(self, dt):
        self.score += dt / 1000  # Score por tempo

    def draw_hud(self, clock):
        self.level_text(14, f'{self.name} - Time Left: {self.time_left // 1000}s', C_WHITE, (10, 5))
        self.level_text(14, f'Score: {int(self.score)}', C_WHITE, (10, 25))
        self.level_text(14, f'Entities: {len(self.entities)}', C_WHITE, (10, 45))
        self.level_text(14, f'FPS: {clock.get_fps():.0f}', C_WHITE, (10, WIN_HEIGHT - 35))

    def run(self):
        clock = pygame.time.Clock()
        pygame.mixer_music.stop()
        pygame.mixer_music.load('./asset/Level1.mp3')
        pygame.mixer_music.play(-1)
        running = True

        while running:
            dt = clock.tick(60)
            self.spawn_timer += dt
            self.time_left -= dt

            # Eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        bullet = self.player.shoot()
                        self.bullets.add(bullet)
                        pygame.mixer.Sound.play(self.shoot_sound)

            # Atualizações
            self.update_player()
            self.update_bullets()
            self.spawn_entities()
            self.move_entities()
            self.check_collisions()
            self.update_score(dt)

            # Condições de término
            if not self.player.is_alive:
                self.fade_in_text("Game Over", 40, (255, 0, 0))
                pygame.display.flip()
                pygame.time.delay(1500)
                return self.menu_return

            if self.time_left <= 0 and self.player.is_alive:
                from code.Level2 import Level2
                next_level = Level2(self.window, self.score, self.menu_return)
                next_level.run()
                return

            # Render
            self.update()
            self.draw()
            self.draw_hud(clock)
            pygame.display.flip()

    def draw_health_bar(self):
        if not self.player.is_alive:
            return
        bar_width = 200
        bar_height = 5
        x, y = 10, 70

        ratio = max(self.player.health, 0) / 200
        fill_width = int(bar_width * ratio)

        pygame.draw.rect(self.window, (255, 0, 0), (x, y, bar_width, bar_height))
        pygame.draw.rect(self.window, (0, 255, 0), (x, y, fill_width, bar_height))

    def level_text(self, text_size: int, text: str, text_color: tuple, text_pos: tuple, centered=False):
        font = pygame.font.SysFont("Lucida Sans Typewriter", text_size)
        surf = font.render(text, True, text_color).convert_alpha()

        if centered:
            rect = surf.get_rect(center=text_pos)  # centraliza no ponto
        else:
            rect = surf.get_rect(topleft=text_pos)  # mantém padrão à esquerda

        self.window.blit(surf, rect)

    def update(self):
        for i, entity in enumerate(self.entity_list):
            self.layer_offsets[i] -= self.layer_speeds[i]
            width = entity.surf.get_width()
            if self.layer_offsets[i] <= -width:
                self.layer_offsets[i] = 0

    def fade_in_text(self, text: str, size: int, color: tuple, duration=2000):
        font = pygame.font.SysFont("Lucida Sans Typewriter", size)
        surf = font.render(text, True, color).convert_alpha()
        rect = surf.get_rect(center=(self.window.get_width() // 2, self.window.get_height() // 2))

        clock = pygame.time.Clock()
        total_time = 0
        alpha = 0

        while total_time < duration:
            dt = clock.tick(60)
            total_time += dt
            alpha = min(255, int((total_time / duration) * 255))
            surf.set_alpha(alpha)

            self.update()
            self.draw()
            self.window.blit(surf, rect)
            pygame.display.flip()

    def draw(self):
        for i, entity in enumerate(self.entity_list):
            offset = self.layer_offsets[i]
            width = entity.surf.get_width()
            self.window.blit(entity.surf, (offset, 0))
            self.window.blit(entity.surf, (offset + width, 0))
            self.level_text(14, f'Health: {self.player.health}', C_WHITE, (10, 70))

        if self.player.is_alive:
            self.window.blit(self.player.image, self.player.rect)

        for entity in self.entities:
            self.window.blit(entity.surf, entity.rect)

        self.bullets.draw(self.window)
