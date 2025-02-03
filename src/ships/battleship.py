from radars.base import Radar

from .base import Ship


class Battleship(Ship):
    def __init__(self, sprite_path: str, radar: Radar):
        super().__init__(sprite_path, damage=20, health=50, speed=2, radar=radar)

    def receive_damage(self, damage: float, distance: float) -> None:
        print('{} должен получить {} урон(-а) с дистанции {}'.format(str(self), damage, distance))
        if damage <= 10:
            damage = 0

        print('{} получил {} урон(-а) с дистанции {}'.format(str(self), damage, distance))

        self.health -= damage

    def __str__(self):
        return 'линкор'
