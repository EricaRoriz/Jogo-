from code.Background import Background
from code.Player import Player
from code.StaticObstacle import StaticObstacle


class EntityFactory:

    @staticmethod
    def get_entity(entity_name: str, position=(0, 0)):
        if entity_name == 'Level1Bg':
            return [Background(f'Level1Bg{i}', position) for i in range(9)]

        elif entity_name == 'Level2Bg':
            return [Background(f'Level2Bg{i}', position) for i in range(7)]

        elif entity_name == 'Player1':
            pos = position if position != (0, 0) else (10, 680)
            return Player('Player1', pos)

        elif entity_name == 'Obstacle':
            # Obstáculos Level 1, tamanho original
            return [
                StaticObstacle('Hand', (150, 220), size=(80, 100)),
                StaticObstacle('Lapide', (250, 220), size=(80, 100)),
                StaticObstacle('Bones', (350, 220), size=(80, 100))
            ]

        elif entity_name == 'ObstacleLevel2':
            # Obstáculos Level 2, com tamanho reduzido
            return [
                StaticObstacle('Hand2', (150, 220), size=(70, 90), speed=6),
                StaticObstacle('Abobora', (250, 240), size=(60, 80), speed=6),
                StaticObstacle('Placa', (350, 220), size=(70, 90), speed=6),
                StaticObstacle('Barril', (450, 240), size=(70, 90), speed=6)
            ]

        else:
            return None
