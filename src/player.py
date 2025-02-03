from typing import List
from ships import Ship


class Player:
    def __init__(self, name: str, ships: List[Ship]):
        self.name = name
        self.ships = ships
        self.selected_ship: Ship = None

    def get_ships(self) -> List[Ship]:
        return self.ships

    def remove_ship(self, ship: Ship) -> None:
        self.ships.remove(ship)

    def set_selected_ship(self, ship: Ship):
        self.selected_ship = ship

    def get_selected_ship(self) -> Ship:
        return self.selected_ship
