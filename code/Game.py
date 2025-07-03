#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame

from code.Level import Level
from code.Level2 import Level2  # IMPORTANTE
from code.Menu import Menu
from code.const import WIN_WIDTH, WIN_HEIGHT, MENU_OPTION


class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode(size=(WIN_WIDTH, WIN_HEIGHT))

    def run(self):
        while True:
            menu = Menu(self.window)
            menu_return = menu.run()

            if menu_return in [MENU_OPTION[0], MENU_OPTION[1], MENU_OPTION[2]]:
                level = Level(self.window, 'Level 1', menu_return)
                level_return = level.run()
                if level_return == menu_return:
                    continue  # Volta ao menu

            elif menu_return == MENU_OPTION[4]:
                pygame.quit()
                quit()
