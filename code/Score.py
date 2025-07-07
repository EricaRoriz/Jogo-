from datetime import datetime

import pygame
from pygame import Surface, Rect
from pygame.examples.music_drop_fade import volume
from pygame.font import Font

from code.DBProxy import DBProxy
from code.const import WIN_WIDTH, WIN_HEIGHT, C_YELLOW, SCORE_POS, MENU_OPTION, C_WHITE


class Score:

    def __init__(self, window: Surface, bg_path: str = './asset/Score_bg.png'):
        self.window = window
        original_surf = pygame.image.load(bg_path).convert_alpha()
        self.surf = pygame.transform.scale(original_surf, (701, 458))
        self.rect = self.surf.get_rect(left=0, top=0)
        pass

    def save(self, menu_return: str, player_score: list[int]):
        pygame.mixer_music.load('./asset/Score.mp3')
        pygame.mixer_music.set_volume(0.5)
        pygame.mixer_music.play(-1)
        db_proxy = DBProxy('DBScore.db')

        score_data = {
            'name': 'USER',
            'score': player_score[0],
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        db_proxy.save(score_data)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False

            self.window.blit(source=self.surf, dest=self.rect)
            self.score_text(48, 'YOU WIN!', C_YELLOW, SCORE_POS['Title'])
            if menu_return == MENU_OPTION[0]:
                self.score_text(24, 'Player 1 enter your name (4 characters):', C_WHITE, SCORE_POS['Enter Name'])

            pygame.display.flip()

    def show(self):
        pygame.mixer_music.load('./asset/Score.mp3')
        pygame.mixer_music.set_volume(volume)
        pygame.mixer_music.play(-1)

        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False

            self.window.fill((0, 0, 0))
            self.window.blit(source=self.surf, dest=self.rect)
            self.score_text(72, 'YOU WIN!', C_YELLOW, SCORE_POS['Title'])
            self.score_text(24, 'Press ESC to return', C_WHITE, (WIN_WIDTH / 2, WIN_HEIGHT - 30))
            pygame.display.flip()

    def score_text(self, text_size: int, text: str, text_color: tuple, text_center_pos: tuple):
        text_font: Font = pygame.font.SysFont(name="Lucida Sans Typerwriter", size=text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(center=text_center_pos)
        self.window.blit(source=text_surf, dest=text_rect)
