# code/EntityFactory.py
from code.Background import Background
from code.StaticObstacle import StaticObstacle
from code.Player import Player
from code.const import WIN_WIDTH, WIN_HEIGHT


# code/EntityFactory.py
from code.Background import Background
from code.StaticObstacle import StaticObstacle
from code.Player import Player
from code.const import WIN_WIDTH, WIN_HEIGHT


class EntityFactory:

    @staticmethod
    def get_entity(entity_name: str, position=(0, 0)):
        if entity_name == 'Level1Bg':
            return [Background(f'Level1Bg{i}', position) for i in range(9)]

        elif entity_name == 'Player1':
            pos = position if position != (0, 0) else (10, 680)
            return Player('Player1', pos)

        elif entity_name == 'Obstacle':
            return [
                StaticObstacle('Hand', (150, 220), size=(80, 100)),
                StaticObstacle('Lapide', (250, 220), size=(80, 100)),
                StaticObstacle('Bones', (350, 220), size=(80, 100))
            ]

        else:
            return None
