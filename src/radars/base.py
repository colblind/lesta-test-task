from abc import ABC, abstractmethod
from math import floor
from typing import List, TYPE_CHECKING, TypedDict

from board import Board


if TYPE_CHECKING:
    from ships.base import Ship


class TargetData(TypedDict):
    target: "Ship"
    distance: float


class Radar(ABC):
    def __init__(self, board: Board):
        self.board = board

    @abstractmethod
    def find_targets(self, attacker: "Ship", targets: List["Ship"]) -> List[TargetData]:
        pass

    def calculate_damage(self, attacker: "Ship", targets: List["Ship"]) -> float:
        if not targets:
            return 0

        return floor(attacker.damage / len(targets))

    def _calculate_distance(self, pos1: tuple, pos2: tuple) -> float:
        x1, y1 = pos1
        x2, y2 = pos2
        return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
