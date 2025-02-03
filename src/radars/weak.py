from typing import List

from board import Board

from radars.base import Radar, TargetData
from ships.base import Ship


class WeakRadar(Radar):
    def __init__(self, board: Board):
        super().__init__(board)

    def find_targets(self, attacker: Ship, targets: List[Ship]) -> List[TargetData]:
        attack_range = self.board.get_neighbors(attacker.position[0], attacker.position[1])
        targets_in_range = []
        for target in targets:
            if (target.position[0], target.position[1]) in attack_range:
                targets_in_range.append({"target": target, "distance": 1})
        return targets_in_range
