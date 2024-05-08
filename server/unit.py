from random import randint
from constants import *


class Unit:
    def __init__(
        self,
        owner: str,
        hp: int,
        movement_chance: int,
        attack_chance: int,
        attack_range: int,
        attack_dmg: int,
        type: UnitType,
    ):
        self.owner: str = owner
        self.hp: int = hp
        self.movement_chance: int = movement_chance
        self.attack_chance: int = attack_chance
        self.attack_range: int = attack_range
        self.attack_dmg: int = attack_dmg
        self.maxHP: int = hp
        self.type: UnitType = type

    def move(self) -> bool:
        return randint(1, 100) <= self.movement_chance

    def attack(self) -> bool:
        return randint(1, 100) <= self.attack_chance

    def get_data(self) -> str:
        stats = (
            self.owner,
            self.hp,
            self.movement_chance,
            self.attack_chance,
            self.attack_range,
            self.attack_dmg,
            self.type.value,
        )
        return " ".join(map(str, stats))

    def observe(self) -> str:
        return " ".join(map(str, (self.owner, self.hp, self.maxHP, self.type.value)))

    def __str__(self):
        return f"U({self.type}, {self.owner}, hp={self.hp})"

    def __repr__(self):
        return f"U({self.type}, {self.owner}, hp={self.hp}, mc={self.movement_chance}, ac={self.attack_chance}, ar={self.attack_range}, ad={self.attack_dmg})"


class Melee(Unit):
    def __init__(self, owner: str, upgrades : list[bool]):
        super().__init__(
            owner,
            unit_hp[UnitType.BAGER.value][upgrades[Upgrade.HEALTH.value]],
            unit_move_chance[UnitType.BAGER.value],
            unit_attack_chance[UnitType.BAGER.value][upgrades[Upgrade.ATTACK_CHANCE.value]],
            unit_range[UnitType.BAGER.value],
            unit_attack_dmg[UnitType.BAGER.value][upgrades[Upgrade.ATTACK_DMG.value]],
            UnitType.BAGER,
        )


class Ranged(Unit):
    def __init__(self, owner: str, upgrades : list[bool]):
        super().__init__(
            owner,
            unit_hp[UnitType.DVIHAK.value][upgrades[Upgrade.HEALTH.value]],
            unit_move_chance[UnitType.DVIHAK.value],
            unit_attack_chance[UnitType.DVIHAK.value][upgrades[Upgrade.ATTACK_CHANCE.value]],
            unit_range[UnitType.DVIHAK.value],
            unit_attack_dmg[UnitType.DVIHAK.value][upgrades[Upgrade.ATTACK_DMG.value]],
            UnitType.DVIHAK,
        )


class Tank(Unit):
    def __init__(self, owner: str, upgrades : list[bool]):
        super().__init__(
            owner,
            unit_hp[UnitType.VALEC.value][upgrades[Upgrade.HEALTH.value]],
            unit_move_chance[UnitType.VALEC.value],
            unit_attack_chance[UnitType.VALEC.value][upgrades[Upgrade.ATTACK_CHANCE.value]],
            unit_range[UnitType.VALEC.value],
            unit_attack_dmg[UnitType.VALEC.value][upgrades[Upgrade.ATTACK_DMG.value]],
            UnitType.VALEC,
        )
