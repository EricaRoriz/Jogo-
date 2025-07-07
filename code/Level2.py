import sys
import pygame
import sqlite3
from datetime import datetime

from code.EntityFactory import EntityFactory
from code.Level import Level
from code.Score import Score
from code.const import WIN_WIDTH, WIN_HEIGHT


class Level2(Level):
    def __init__(self, window, score, menu_return):
        super().__init__(window, "LEVEL 2", menu_return)
        self.name = "LEVEL 2"
        self.score = score
        self.entity_list = EntityFactory.get_entity('Level2Bg')
        self.layer_speeds = [0.3 + i * 1.5 for i in range(len(self.entity_list))]
        self.obstacle_types = ['Barril', 'Abobora', 'Placa', 'Hand2']

        # Conecta ao banco SQLite e cria tabela se não existir
        self.conn = sqlite3.connect('DBScore.db')
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS dados(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                score INTEGER NOT NULL,
                date TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def save_score(self, player_name, score):
        self.conn.execute(
            'INSERT INTO dados (name, score, date) VALUES (?, ?, ?)',
            (player_name, score, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        )
        self.conn.commit()

    def close_db(self):
        self.conn.close()

    def run(self):
        clock = pygame.time.Clock()
        running = True

        pygame.mixer_music.stop()
        pygame.mixer_music.load('./asset/Level2.mp3')
        pygame.mixer_music.play(-1)

        while running:
            dt = clock.tick(60)
            self.spawn_timer += dt
            self.time_left -= dt

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.close_db()
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and self.player.is_alive:
                        bullet = self.player.shoot()
                        self.bullets.add(bullet)
                        pygame.mixer.Sound.play(self.shoot_sound)

            self.update_player()
            self.update_bullets()
            self.spawn_entities()
            self.move_entities()
            self.check_collisions()
            self.update_score(dt)

            # Game over - salva score no banco
            if not self.player.is_alive:
                self.fade_in_text("Game Over", 40, (255, 0, 0))
                pygame.display.flip()
                pygame.time.delay(1500)
                score_screen = Score(self.window)
                score_screen.save(self.menu_return, [int(self.score)])
                return self.menu_return

            # Vitória
            if self.time_left <= 0:
                self.window.fill((0, 0, 0))
                self.fade_in_text("Parabéns! Você venceu o jogo!", 36, (0, 255, 0))
                pygame.display.flip()
                pygame.time.delay(3000)
                score_screen = Score(self.window)
                score_screen.save(self.menu_return, [int(self.score)])
                return

            # Render
            self.update()
            self.draw()
            self.draw_hud(clock)
            pygame.display.flip()
