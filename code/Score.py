import sqlite3
from datetime import datetime

import pygame
from pygame import Surface, Rect
from pygame.font import Font

from code.const import WIN_WIDTH, WIN_HEIGHT, C_YELLOW, SCORE_POS, MENU_OPTION, C_WHITE


class Score:

    def __init__(self, window: Surface, bg_path: str = './asset/Score_bg.png'):
        self.window = window
        original_surf = pygame.image.load(bg_path).convert_alpha()
        self.surf = pygame.transform.scale(original_surf, (702, 459))
        self.rect = self.surf.get_rect(left=0, top=0)

    def save(self, menu_return: str, player_score: list[int]):
        pygame.mixer_music.load('./asset/Score.mp3')
        pygame.mixer_music.set_volume(0.5)
        pygame.mixer_music.play(-1)

        input_text = ''
        font = pygame.font.SysFont("Lucida Sans Typewriter", 32)
        active = True

        while active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and len(input_text) > 0:
                        # Salvar score no banco
                        conn = sqlite3.connect('DBScore.db')
                        conn.execute('INSERT INTO dados (name, score, date) VALUES (?, ?, ?)', (
                            input_text.upper(),
                            player_score[0],
                            datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        ))
                        conn.commit()
                        conn.close()
                        active = False
                        self.show()
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    elif len(input_text) < 4 and event.unicode.isalnum():
                        input_text += event.unicode

            # Desenha tela de entrada de nome
            self.window.blit(self.surf, self.rect)
            self.score_text(48, 'YOU WIN!', C_YELLOW, SCORE_POS['Title'])
            self.score_text(24, 'Player enter your name (4 characters):', C_WHITE, SCORE_POS['Enter Name'])

            input_surf = font.render(input_text.upper(), True, C_YELLOW)
            input_rect = input_surf.get_rect(center=(WIN_WIDTH / 2, SCORE_POS['Enter Name'][1] + 40))
            self.window.blit(input_surf, input_rect)

            pygame.display.flip()

    def show(self):
        pygame.mixer_music.load('./asset/Score.mp3')
        pygame.mixer_music.set_volume(0.5)
        pygame.mixer_music.play(-1)

        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False

            self.window.fill((0, 0, 0))
            self.window.blit(self.surf, self.rect)
            self.score_text(38, 'YOU WIN!', C_YELLOW, (WIN_WIDTH / 2, 35))

            # Exibe o ranking Top 10
            top_scores = self.get_top_scores()
            # Título
            self.score_text(24, 'TOP 10 SCORE', C_YELLOW, (WIN_WIDTH / 2, 70))

            # Cabeçalhos
            self.score_text(20, 'NAME', C_YELLOW, (WIN_WIDTH / 4, 100))
            self.score_text(20, 'SCORE', C_YELLOW, (WIN_WIDTH / 2, 100))
            self.score_text(20, 'DATE', C_YELLOW, (3 * WIN_WIDTH / 4, 100))

            # Dados
            for i, (name, score, date) in enumerate(top_scores):
                y_pos = 130 + i * 28  # Mais compacto
                time_str = datetime.strptime(date, "%Y-%m-%d %H:%M:%S").strftime("%H:%M - %d/%m/%y")
                self.score_text(20, name.upper(), C_WHITE, (WIN_WIDTH / 4, y_pos))
                self.score_text(20, f"{score:05}", C_WHITE, (WIN_WIDTH / 2, y_pos))
                self.score_text(20, time_str, C_WHITE, (3 * WIN_WIDTH / 4, y_pos))

            self.score_text(20, 'Press ESC to return', C_WHITE, (WIN_WIDTH / 2, WIN_HEIGHT - 30))
            pygame.display.flip()

    def get_top_scores(self, limit=10):
        conn = sqlite3.connect('DBScore.db')
        cursor = conn.execute('SELECT name, score, date FROM dados ORDER BY score DESC LIMIT ?', (limit,))
        scores = cursor.fetchall()
        conn.close()
        return scores

    def score_text(self, text_size: int, text: str, text_color: tuple, text_center_pos: tuple):
        text_font: Font = pygame.font.SysFont("Lucida Sans Typewriter", text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(center=text_center_pos)
        self.window.blit(text_surf, text_rect)
