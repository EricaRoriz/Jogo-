#!/usr/bin/python
# -*- coding: utf-8 -*-
from msilib.schema import Font

import pygame
from pygame import Surface, Rect

from code.const import WIN_WIDTH, C_RED, MENU_OPTION, C_WHITE, C_YELLOW


class Menu:
    def __init__(self, window):
        self.window = window
        self.surf = pygame.image.load('./asset/BgMenu.png').convert_alpha()
        self.rect = self.surf.get_rect(left=0, top=0)

    def run(self):
        menu_option = 0
        volume = 0.5
        muted = False
        pygame.mixer_music.load('./asset/Menu_music.wav')
        pygame.mixer_music.set_volume(volume)
        pygame.mixer_music.play(-1)

        while True:
            self.window.blit(source=self.surf, dest=self.rect)
            self.menu_text(90, "Zombie", C_RED, ((WIN_WIDTH / 2), 90))
            self.menu_text(90, "Shooter", C_RED, ((WIN_WIDTH / 2), 160))

            for i in range(len(MENU_OPTION)):
                color = C_YELLOW if i == menu_option else C_WHITE
                self.menu_text(30, MENU_OPTION[i], color, ((WIN_WIDTH / 2), 250 + 30 * i))

            # Mostra volume/mute
            volume_display = "MUTE" if muted else f"Volume: {int(volume * 100)}%"
            self.menu_text(20, volume_display, C_WHITE, (WIN_WIDTH / 2, 420))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        menu_option = (menu_option + 1) % len(MENU_OPTION)
                    elif event.key == pygame.K_UP:
                        menu_option = (menu_option - 1) % len(MENU_OPTION)

                    elif event.key == pygame.K_RETURN:
                        if MENU_OPTION[menu_option] == "OPTIONS":
                            self.run_options_menu()
                        elif MENU_OPTION[menu_option] == "EXIT":
                            pygame.quit()
                            quit()
                        else:
                            return MENU_OPTION[menu_option]

                    elif event.key == pygame.K_m:
                        muted = not muted
                        pygame.mixer_music.set_volume(0.0 if muted else volume)
                    elif event.key == pygame.K_RIGHT:
                        if not muted and volume < 1.0:
                            volume = min(1.0, volume + 0.1)
                            pygame.mixer_music.set_volume(volume)
                    elif event.key == pygame.K_LEFT:
                        if not muted and volume > 0.0:
                            volume = max(0.0, volume - 0.1)
                            pygame.mixer_music.set_volume(volume)

    def menu_text(self, text_size: int, text: str, text_color: tuple, text_center_pos: tuple):
        text_font: Font = pygame.font.SysFont(name="Lucida Sans Typerwriter", size=text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(center=text_center_pos)
        self.window.blit(source=text_surf, dest=text_rect)

    def run_options_menu(self):
        volume = pygame.mixer_music.get_volume()
        muted = volume == 0.0
        running = True

        while running:
            self.window.blit(self.surf, self.rect)
            self.menu_text(60, "OPTIONS", C_RED, (WIN_WIDTH / 2, 100))

            status = "Muted" if muted else f"Volume: {int(volume * 100)}%"
            self.menu_text(40, status, C_WHITE, (WIN_WIDTH / 2, 200))
            self.menu_text(30, "LEFT: decrease | RIGHT: increase | M to mute | ESC to return", C_WHITE, (WIN_WIDTH / 2, 260))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_m:
                        muted = not muted
                        pygame.mixer_music.set_volume(0.0 if muted else volume)
                    elif event.key == pygame.K_RIGHT and not muted:
                        volume = min(1.0, volume + 0.1)
                        pygame.mixer_music.set_volume(volume)
                    elif event.key == pygame.K_LEFT and not muted:
                        volume = max(0.0, volume - 0.1)
                        pygame.mixer_music.set_volume(volume)


def run(self, ):
    pass
