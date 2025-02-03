from typing import List

from obstacles import HighIsland
from ships import Ship, Destroyer, Cruiser, Battleship
from board import Board
import math


class Combat:
    def __init__(self, board: Board):
        self.board = board

    def attack(self, attacker: Ship, targets: List[Ship]) -> None:
        print('{} is attacking'.format(attacker))

        if not targets:
            return

        if isinstance(attacker, Destroyer):
            self._destroyer_attack(attacker, targets)
        elif isinstance(attacker, Cruiser):
            self._cruiser_attack(attacker, targets)
        elif isinstance(attacker, Battleship):
            self._battleship_attack(attacker, targets)

    def _destroyer_attack(self, destroyer: Destroyer, targets: List[Ship]) -> None:
        attack_range = self.board.get_neighbors(destroyer.position[0], destroyer.position[1])
        targets_in_range = []
        for target in targets:
            if (target.position[0], target.position[1]) in attack_range:
                targets_in_range.append(target)

        if not targets_in_range:
            return

        damage_per_target = math.floor(destroyer.damage / len(targets_in_range))
        if damage_per_target:
            self._deal_damage(destroyer, damage_per_target, targets_in_range)

    def _cruiser_attack(self, cruiser: Cruiser, targets: List[Ship]) -> None:
        targets_in_range = self._get_targets_in_line_of_sight(cruiser, targets)

        if not targets_in_range:
            return

        damage_per_target = math.floor(cruiser.damage / len(targets_in_range))

        if damage_per_target:
            self._deal_damage(cruiser, damage_per_target, targets_in_range)

    def _battleship_attack(self, battleship: Battleship, targets: List[Ship]) -> None:
        targets_in_range = self._get_targets_in_line_of_sight(battleship, targets)

        if not targets_in_range:
            return

        damage_per_target = math.floor(battleship.damage / len(targets_in_range))

        if damage_per_target:
            self._deal_damage(battleship, damage_per_target, targets_in_range)

    def _deal_damage(self, attacker, damage_per_target: float, victims: list[Ship]) -> None:
        if not damage_per_target:
            return

        targets_count = len(victims)
        for target in victims:
            damage = damage_per_target
            if isinstance(target, Cruiser) or isinstance(target, Destroyer):
                distance = self._calculate_distance(attacker.position, target.position)
                if distance > 2:
                    print('{} должен получить {} урон(-а)'.format(target, damage_per_target))
                    damage = math.floor(damage / 2)
            elif isinstance(target, Battleship):
                print('{} должен получить {} урон(-а)'.format(target, damage))
                if damage <= 10:
                    damage = 0
            print('{} получает {} урон(-а)'.format(target, damage))
            target.receive_damage(math.floor(damage / targets_count))

    def _get_targets_in_line_of_sight(self, attacker: Ship, targets: List[Ship]) -> List[Ship]:
        targets_in_range = []
        for target in targets:
            if self._is_in_same_line(attacker.position, target.position) and not self._is_blocked(attacker.position,
                                                                                                  target.position):
                targets_in_range.append(target)
        return targets_in_range

    def _is_blocked(self, pos1: tuple, pos2: tuple) -> bool:
        x1, y1 = pos1
        x2, y2 = pos2

        if x1 == x2:
            start, end = min(y1, y2), max(y1, y2)
            for y in range(start + 1, end):
                obj = self.board.get_object(x1, y)
                if obj and isinstance(obj, HighIsland):
                    return True
        elif y1 == y2:
            start, end = min(x1, x2), max(x1, x2)
            for x in range(start + 1, end):
                obj = self.board.get_object(x, y1)
                if obj and isinstance(obj, HighIsland):
                    return True
        return False

    def _is_in_same_line(self, pos1: tuple, pos2: tuple) -> bool:
        x1, y1 = pos1
        x2, y2 = pos2
        return x1 == x2 or y1 == y2

    def _calculate_distance(self, pos1: tuple, pos2: tuple) -> float:
        x1, y1 = pos1
        x2, y2 = pos2
        return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
