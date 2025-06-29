#!/usr/bin/python
# -*- coding: utf-8 -*-
from msilib.schema import Font

import pygame
from pygame import Surface, Rect

from code.const import WIN_WIDTH, C_RED, MENU_OPTION, C_WHITE


class Menu:
    def __init__(self, window):
        self.window = window
        self.surf = pygame.image.load('./asset/BgMenu.png')
        self.rect = self.surf.get_rect(left=0, top=0)

    def run(self):
        pygame.mixer_music.load('./asset/Menu_music.wav')
        pygame.mixer_music.play(-1)
        while True:
            self.window.blit(source=self.surf, dest=self.rect)
            self.menu_text(90, "Zombie", C_WHITE, ((WIN_WIDTH / 2), 90))
            self.menu_text(90, "Shooter", C_WHITE, ((WIN_WIDTH / 2), 160))

            for i in range(len(MENU_OPTION)):
                self.menu_text(30, MENU_OPTION[i], C_WHITE, ((WIN_WIDTH / 2), 250 + 30 * i))

            pygame.display.flip()

            # Check for all events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()  # Close Window
                    quit()  # end pygame

    def menu_text(self, text_size: int, text: str, text_color: tuple, text_center_pos: tuple):
        text_font: Font = pygame.font.SysFont(name="Lucida Sans Typerwriter", size=text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(center=text_center_pos)
        self.window.blit(source=text_surf, dest=text_rect)


def run(self, ):
    pass
