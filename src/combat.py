from typing import List

from radars.base import TargetData
from ships.base import Ship


class Combat:
    @classmethod
    def attack(cls, attacker: Ship, targets: List[Ship]) -> None:
        print('{} is attacking'.format(attacker))

        if not targets:
            return

        targets_in_range = attacker.radar.find_targets(attacker, targets)

        damage_per_target = attacker.radar.calculate_damage(attacker, [target_data.get("target") for target_data in targets_in_range])

        cls._deal_damage(damage_per_target, targets_in_range)

    @classmethod
    def _deal_damage(cls, damage_per_target: float, targets_in_range: list[TargetData]) -> None:
        if not damage_per_target:
            return

        for target_data in targets_in_range:
            target = target_data.get("target")
            distance = target_data.get("distance")

            target.receive_damage(damage_per_target, distance)
