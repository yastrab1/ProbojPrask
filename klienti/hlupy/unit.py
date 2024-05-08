from constants import UnitType


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
        self.owner = owner
        self.hp = hp
        self.movement_chance = movement_chance
        self.attack_chance = attack_chance
        self.attack_range = attack_range
        self.attack_dmg = attack_dmg
        self.type = type
