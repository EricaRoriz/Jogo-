import pygame.sprite


class ModularPlayer(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.head = pygame.image.load('./asset/player/Head.png').convert_alpha()
        self.bodies = [
            pygame.image.load('./asset/player/PlayerBody0.png').convert_alpha(),
            pygame.image.load('./asset/player/PlayerBody0.png').convert_alpha()
            ]
        self.run_frames = [
            pygame.image.load('./asset/player/PlayerRun0.png').convert_alpha(),
            pygame.image.load('./asset/player/PlayerRun1.png').convert_alpha(),
            pygame.image.load('./asset/player/PlayerRun2.png').convert_alpha(),
            pygame.image.load('./asset/player/PlayerRun3.png').convert_alpha(),
            pygame.image.load('./asset/player/PlayerRun4.png').convert_alpha(),
            pygame.image.load('./asset/player/PlayerRun5.png').convert_alpha(),
            pygame.image.load('./asset/player/PlayerRun6.png').convert_alpha(),
            pygame.image.load('./asset/player/PlayerRun7.png').convert_alpha()
        ]
        self.jump_frames = [
            pygame.image.load('./asset/player/PlayerJump0.png').convert_alpha(),
            pygame.image.load('./asset/player/PlayerJump1.png').convert_alpha()
        ]
        self.current_frames = 0
        self.frame_timer = 0
        self.state = "idle"

        self.image = self.bodies[0]
        self.rect = self.image.get_rect(topleft=position)

        self.health = 200
        self.is_alive = True

    def update(self, keys):
        if not self.is_alive:
            return

        if keys[pygame.K_RIGHT] or keys [pygame.K_LEFT]:
            self.state = "run"
        else:
            self.state = "idle"

        self.frame_timer += 1
        if self.frame_timer > 6:
            self.current_frames = (self.current_frames + 1) % 8
            self.frame_timer = 0

        if self.state == "run":
            self.image = self.run_frames[self.current_frames]
        elif self.state == "idle":
            self.image = self.bodies[0]


