import sys

import pygame

from code.EntityFactory import EntityFactory
from code.Level import Level
from code.const import WIN_WIDTH, WIN_HEIGHT


class Level2(Level):
    def __init__(self, window, score, menu_return):
        super().__init__(window, "LEVEL 2", menu_return)
        self.name = "LEVEL 2"
        self.score = score
        self.entity_list = EntityFactory.get_entity('Level2Bg')
        self.layer_speeds = [0.3 + i * 1.5 for i in range(len(self.entity_list))]
        self.obstacle_types = ['Barril', 'Abobora', 'Placa', 'Hand2']

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

            # Atualizações
            self.update_player()
            self.update_bullets()
            self.spawn_entities()
            self.move_entities()
            self.check_collisions()
            self.update_score(dt)

            # Condições de término
            if not self.player.is_alive:
                self.fade_in_text("Game Over", 40, (255, 0, 0))
                pygame.display.flip()
                pygame.time.delay(1500)
                return self.menu_return

            if self.time_left <= 0:
                self.window.fill((0, 0, 0))
                self.fade_in_text("Parabéns! Você venceu o jogo!", 36, (0, 255, 0))
                pygame.time.delay(1000)

                pygame.display.flip()
                pygame.time.delay(3000)
                return self.menu_return

            # Render
            self.update()
            self.draw()
            self.draw_hud(clock)
            pygame.display.flip()
