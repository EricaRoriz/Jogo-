#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame

from code.Level import Level
from code.Level2 import Level2
from code.Menu import Menu
from code.Score import Score
from code.const import WIN_WIDTH, WIN_HEIGHT, MENU_OPTION


class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode(size=(WIN_WIDTH, WIN_HEIGHT))

    def run(self):
        while True:
            score = Score(self.window)
            menu = Menu(self.window)
            menu_return = menu.run()

            if menu_return == MENU_OPTION[0]:  # START
                player_score = [0, 0]

                # Level 1
                level1 = Level(self.window, 'Level 1', menu_return)
                level1_return = level1.run()

                if level1_return == "GAME_OVER":
                    continue  # volta para o menu

                if level1_return == "VICTORY":
                    player_score[0] = int(level1.score)

                    # Level 2
                    level2 = Level2(self.window, player_score[0], menu_return)
                    level2_return = level2.run()

                    if level2_return == "GAME_OVER":
                        continue  # volta para o menu

                    if level2_return == "VICTORY":
                        player_score[1] = int(level2.score)
                        score.save(menu_return, player_score)
                        continue  # volta para o menu

                player_score[1] = int(level2.score)
                score.save(menu_return, player_score)

            elif menu_return == MENU_OPTION[1]:  # SCORE
                score.show()

            elif menu_return == MENU_OPTION[2]:  # EXIT
                pygame.quit()
                quit()
