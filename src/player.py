from typing import List
from ships.base import Ship


class Player:
    name: str
    ships: List[Ship]
    selected_ship: Ship | None

    def __init__(self, name: str, ships: List[Ship]):
        self.name = name
        self.ships = ships
        self.selected_ship = None

    def get_ships(self) -> List[Ship]:
        return self.ships

    def remove_ship(self, ship: Ship) -> None:
        self.ships.remove(ship)

    def set_selected_ship(self, ship: Ship | None) -> None:
        self.selected_ship = ship

    def get_selected_ship(self) -> Ship:
        return self.selected_ship
