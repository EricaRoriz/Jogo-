from idlelib import window

import pygame
from pygame import Surface
from pygame.examples.music_drop_fade import volume

from code.const import WIN_WIDTH, WIN_HEIGHT


class Score:

    def __init__(self, window: Surface, bg_path:str = './asset/Score_bg.png'):
        self.window = window
        original_surf = pygame.image.load(bg_path).convert_alpha()
        self.surf = pygame.transform.scale(original_surf, (701, 458))
        self.rect = self.surf.get_rect(left=0, top=0)
        pass

    def save(self, menu_return: str, player_score: list[int]):
        pygame.mixer_music.load('./asset/Score.mp3')
        pygame.mixer_music.set_volume(volume)
        pygame.mixer_music.play(-1)
        self.window.blit(source=self.surf, dest=self.rect)
        while True:
            pygame.display.flip()
            pass

        pass

    def show(self):
        pygame.mixer_music.load('./asset/Score.mp3')
        pygame.mixer_music.set_volume(volume)
        pygame.mixer_music.play(-1)
        self.window.blit(source=self.surf, dest=self.rect)
        while True:
            pygame.display.flip()
            pass


