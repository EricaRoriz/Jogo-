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
        self.time_left = 60000  # 60 segundos em milissegundos
        self.score = 0
        self.last_spawned_type = None

        self.font = pygame.font.SysFont("Lucida Sans Typewriter", 14)

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
            dt = clock.tick(60)  # dt em ms, limita a 60fps

            # Eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and self.player.is_alive:
                        bullet = self.player.shoot()
                        self.bullets.add(bullet)
                        pygame.mixer.Sound.play(self.shoot_sound)

            # Atualiza player
            keys = pygame.key.get_pressed()
            if self.player.is_alive:
                self.player.update(keys)

            # Atualiza balas
            self.bullets.update()
            for bullet in self.bullets.copy():
                if bullet.rect.right < 0 or bullet.rect.left > 701:
                    self.bullets.remove(bullet)
                    continue

                for entity in self.entities[:]:
                    if isinstance(entity, Enemy) and entity.rect.colliderect(bullet.rect):
                        entity.hit()
                        if entity.health <= 0:
                            self.entities.remove(entity)
                            self.score += 10  # Pontos por matar inimigo
                        self.bullets.remove(bullet)
                        break

            # Spawn inimigos e obstáculos alternados
            self.spawn_timer += dt
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
                    new_entity = StaticObstacle(name, (701, 0), size=(70, 90))
                    new_entity.rect.bottom = 440 if name == 'Bones' else 420
                    self.last_spawned_type = 'obstacle'

                self.entities.append(new_entity)
                self.spawn_timer = 0
                self.next_spawn_time = random.randint(1500, 5000)

            # Atualiza entidades (move inimigos/obstáculos)
            for entity in self.entities[:]:
                entity.move()
                if entity.rect.right < 0:
                    self.entities.remove(entity)

            # Colisão player vs inimigos/obstáculos
            if self.player.is_alive:
                for entity in self.entities:
                    if self.player.rect.colliderect(entity.rect):
                        self.player.hit(damage=1)  # dano reduzido
                        # recua para não travar
                        if self.player.rect.left < entity.rect.left:
                            self.player.rect.x -= 10
                        else:
                            self.player.rect.x += 10
                        break

            # Atualiza tempo restante e finaliza o nível se acabar
            self.time_left -= dt
            if self.time_left <= 0:
                print("Tempo esgotado! Fim do nível.")
                running = False

            # Atualiza score com tempo corrido
            self.score += dt / 1000  # 1 ponto por segundo

            # Desenha tudo
            self.update()
            self.draw()

            # HUD
            self.level_text(14, f'{self.name} - Time Left: {self.time_left // 1000}s', C_WHITE, (10, 5))
            self.level_text(14, f'Score: {int(self.score)}', C_WHITE, (10, 25))
            self.level_text(14, f'Entities: {len(self.entities)}', C_WHITE, (10, 45))
            self.level_text(14, f'FPS: {clock.get_fps():.0f}', C_WHITE, (10, WIN_HEIGHT - 35))

            pygame.display.flip()

    def draw_health_bar(self):
        if not self.player.is_alive:
            return
        bar_width = 200
        bar_height = 5
        x, y = 10, 70

        ratio = max(self.player.health, 0) / 200
        fill_width = int(bar_width * ratio)

        # Fundo vermelho
        pygame.draw.rect(self.window, (255, 0, 0), (x, y, bar_width, bar_height))
        # Vida verde
        pygame.draw.rect(self.window, (0, 255, 0), (x, y, fill_width, bar_height))

    def level_text(self, text_size: int, text: str, text_color: tuple, text_pos: tuple):
        font = pygame.font.SysFont("Lucida Sans Typewriter", text_size)
        surf = font.render(text, True, text_color).convert_alpha()
        rect = surf.get_rect(topleft=text_pos)
        self.window.blit(surf, rect)

    def update(self):
        # Atualiza parallax do fundo
        for i, entity in enumerate(self.entity_list):
            self.layer_offsets[i] -= self.layer_speeds[i]
            width = entity.surf.get_width()
            if self.layer_offsets[i] <= -width:
                self.layer_offsets[i] = 0

    def draw(self):
        # Desenha o fundo com parallax
        for i, entity in enumerate(self.entity_list):
            offset = self.layer_offsets[i]
            width = entity.surf.get_width()
            self.window.blit(entity.surf, (offset, 0))
            self.window.blit(entity.surf, (offset + width, 0))
            self.level_text(14, f'Health: {self.player.health}', C_WHITE, (10, 70))

        # Desenha player somente se estiver vivo
        if self.player.is_alive:
            self.window.blit(self.player.surf, self.player.rect)

        # Desenha inimigos e obstáculos
        for entity in self.entities:
            self.window.blit(entity.surf, entity.rect)

        # Desenha as balas
        self.bullets.draw(self.window)
