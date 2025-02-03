from typing import TYPE_CHECKING

from game_object import GameObject


if TYPE_CHECKING:
    from radars.base import Radar


class Ship(GameObject):
    def __init__(self, sprite_path: str, damage: int, health: int, speed: int, radar: "Radar"):
        super().__init__(sprite_path)
        self.damage = damage
        self.health = health
        self.max_health = health
        self.speed = speed
        self.selected = False
        self.position: tuple[int, int] = (-1, -1)
        self.radar = radar

    def receive_damage(self, damage: float, distance: float) -> None:
        self.health -= damage

    def is_alive(self) -> bool:
        return self.health > 0

    def set_position(self, x: int, y: int):
        self.position = (x, y)

    def __str__(self):
        return 'корабль'
