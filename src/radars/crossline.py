from typing import List

from board import Board
from obstacles import Cliff

from radars.base import Radar, TargetData
from ships.base import Ship


class CrossLineRadar(Radar):
    def __init__(self, board: Board):
        super().__init__(board)

    def find_targets(self, attacker: Ship, targets: List[Ship]) -> List[TargetData]:
        targets_in_range = []
        for target in targets:
            if self._is_in_same_line(attacker.position, target.position) and not self._is_blocked(attacker.position,
                                                                                                  target.position):
                targets_in_range.append({"target": target, "distance": self._calculate_distance(attacker.position, target.position)})
        return targets_in_range

    def _is_in_same_line(self, pos1: tuple, pos2: tuple) -> bool:
        x1, y1 = pos1
        x2, y2 = pos2
        return x1 == x2 or y1 == y2

    def _is_blocked(self, pos1: tuple, pos2: tuple) -> bool:
        x1, y1 = pos1
        x2, y2 = pos2

        if x1 == x2:
            start, end = min(y1, y2), max(y1, y2)
            for y in range(start + 1, end):
                obj = self.board.get_object(x1, y)
                if obj and isinstance(obj, Cliff):
                    return True
        elif y1 == y2:
            start, end = min(x1, x2), max(x1, x2)
            for x in range(start + 1, end):
                obj = self.board.get_object(x, y1)
                if obj and isinstance(obj, Cliff):
                    return True
        return False
