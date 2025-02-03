from typing import Tuple

from game_object import GameObject


class Obstacle(GameObject):
    def __init__(self, sprite_path: str):
        super().__init__()
        self.sprite_path = sprite_path
        self.position: Tuple[int, int] = None

    def set_position(self, x: int, y: int):
        self.position = (x, y)

    def __str__(self):
        return 'obstacle'


class HighIsland(Obstacle):
    def __init__(self, sprite_path: str):
        super().__init__(sprite_path)

    def __str__(self):
        return 'high island'


class LowIsland(Obstacle):
    def __init__(self, sprite_path: str):
        super().__init__(sprite_path)

    def __str__(self):
        return 'low island'
