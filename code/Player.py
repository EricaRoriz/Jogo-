#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame
from code.Bullet import Bullet
from code.Entity import Entity


class Player(Entity):
    def __init__(self, position, size=(100, 150)):
        super().__init__('Player/PlayerRun0', position, size)
        scale_body = (85, 125)
        scale_head = (50, 50)
        scale_gun = (60, 30)
        self.frames_run = [pygame.image.load(f'./asset/Player/PlayerRun{i}.png').convert_alpha() for i in range(8)]
        self.frames_run = [pygame.transform.scale(img, size) for img in self.frames_run]
        self.body_image = self.frames_run[0]
        self.head_image = pygame.image.load('./asset/Player/Head.png').convert_alpha()
        self.head_image = pygame.transform.scale(self.head_image, (50, 50))
        self.gun_image = pygame.image.load('./asset/Player/Gun.png').convert_alpha()
        self.gun_image = pygame.transform.scale(self.gun_image, (60, 30))

        self.head_x_offset = 15
        self.head_y_offset = -23
        self.gun_x_offset = 40
        self.gun_y_offset = 30

        self.animation_delay = 5
        self.animation_timer = 0
        self.frame_index = 0

        self.health = 200
        self.is_alive = True
        self.flipped = False
        self.speed = 5
        self.jump_speed = -18
        self.gravity = 1
        self.velocity_y = 0
        self.on_ground = True

        self.image = self.body_image.copy()

        self.compose_image()
        self.rect = self.image.get_rect(topleft=position)

    def hit(self, damage=1):
        if not self.is_alive:
            return
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.is_alive = False

    def update(self, keys_pressed):
        if not self.is_alive:
            return

        moving = False

        if keys_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speed
            self.flipped = True
            moving = True

        if keys_pressed[pygame.K_RIGHT]:
            self.rect.x += self.speed
            self.flipped = False
            moving = True

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 701:
            self.rect.right = 701

        if keys_pressed[pygame.K_UP] and self.on_ground:
            self.velocity_y = self.jump_speed
            self.on_ground = False

        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y

        if self.rect.y >= 285:
            self.rect.y = 285
            self.velocity_y = 0
            self.on_ground = True

        if moving:
            self.animate_run()

        self.compose_image()
        if self.flipped:
            self.image = pygame.transform.flip(self.image, True, False)

    def animate_run(self, gun_y_offset=None):
        self.animation_timer += 1
        if self.animation_timer >= self.animation_delay:
            self.frame_index = (self.frame_index + 1) % len(self.frames_run)
            self.body_image = self.frames_run[self.frame_index]
            self.animation_timer = 0

    def compose_image(self):
        full_height = self.body_image.get_height() + abs(self.head_y_offset)
        width = self.body_image.get_width()
        self.image = pygame.Surface((width, full_height), pygame.SRCALPHA)
        self.image.blit(self.body_image, (0, abs(self.head_y_offset)))
        self.image.blit(self.head_image, (self.head_x_offset, 0))
        self.image.blit(self.gun_image, (self.gun_x_offset, abs(self.head_y_offset) + self.gun_y_offset))

    def move(self):
        pass

    def shoot(self):
        position = self.rect.midright if not self.flipped else self.rect.midleft
        return Bullet(position, self.flipped)

