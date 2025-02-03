from game_object import GameObject


class Ship(GameObject):
    def __init__(self, sprite_path: str, damage: int, health: int, speed: int):
        super().__init__()
        self.sprite_path = sprite_path
        self.damage = damage
        self.health = health
        self.max_health = health
        self.speed = speed
        self.selected = False
        self.position: tuple[int, int] = None

    def receive_damage(self, damage: int) -> None:
        self.health -= damage

    def is_alive(self) -> bool:
        return self.health > 0

    def set_position(self, x: int, y: int):
        self.position = (x, y)

    def __str__(self):
        return 'корабль'


class Destroyer(Ship):
    def __init__(self, sprite_path: str):
        super().__init__(sprite_path, damage=30, health=15, speed=4)

    def __str__(self):
        return 'Эсминец'


class Cruiser(Ship):
    def __init__(self, sprite_path: str):
        super().__init__(sprite_path, damage=15, health=30, speed=3)

    def __str__(self):
        return 'Крейсер'


class Battleship(Ship):
    def __init__(self, sprite_path: str):
        super().__init__(sprite_path, damage=20, health=50, speed=2)

    def __str__(self):
        return 'Линкор'
