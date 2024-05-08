from enum import Enum

map_size: int = 30 # does not include turretes
max_turns: int = 5000
start_money: int = 200

turret_hp: int = 2000
income: list[int] =   [4,  5,   6,   7,   8,   10 ]
income_cost: list[int] = [200, 200, 300, 400, 1500]
turret_cost: list[int] =            [     100, 200, 300, 600, 999]
turret_attack_chance: list[int] =   [ 33,  33,  33,  33,  33,  33]
turret_attack_range: list[int] =    [  2,   2,   5,   8,   8,  11]
turret_dmg: list[int] =             [  5,  10,  20,  20,  25,  30]

unit_cost = [0, 100, 150, 350]
unit_hp = [0, (100, 135), (70, 90), (500, 600)]
unit_move_chance = [0, 50, 50, 33]
unit_attack_chance = [0, (50, 60), (75, 85), (23, 30)]
unit_range = [0, 1, 3, 1]
unit_attack_dmg = [0, (35, 45), (25, 35), (60, 80)]
unit_upgrade_cost = 500


class Command(Enum):
    NONE = 0
    INCOME = 1
    TURRET = 2
    BAGER = 3
    DVIHAK = 4
    VALEC = 5
    HEALTH = 6
    ATTACK_CHANCE = 7
    ATTACK_DMG = 8

class Upgrade(Enum):
    HEALTH = 0
    ATTACK_CHANCE = 1
    ATTACK_DMG = 2


class UnitType(Enum):
    TURRET = 0
    BAGER = 1
    DVIHAK = 2
    VALEC = 3


"""(100, 135) (70, 90) (500, 600)
(50, 60) (75, 85) (23, 30)
(35, 45) (25, 35) (60, 80)"""
