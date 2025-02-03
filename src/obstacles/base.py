from typing import Tuple

from game_object import GameObject


class Obstacle(GameObject):
    def __init__(self, sprite_path: str):
        super().__init__(sprite_path)
        self.position: Tuple[int, int] = (-1, -1)

    def set_position(self, x: int, y: int):
        self.position = (x, y)

    def __str__(self):
        return 'препятствие'
