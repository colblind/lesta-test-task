from math import floor

from radars.base import Radar

from .base import Ship


class Cruiser(Ship):
    def __init__(self, sprite_path: str, radar: Radar):
        super().__init__(sprite_path, damage=15, health=30, speed=3, radar=radar)

    def receive_damage(self, damage: float, distance: float) -> None:
        print('{} должен получить {} урон(-а) с дистанции {}'.format(str(self), damage, distance))
        if distance > 2:
            damage = floor(damage / 2)

        print('{} получил {} урон(-а) с дистанции {}'.format(str(self), damage, distance))

        self.health -= damage

    def __str__(self):
        return 'Крейсер'
