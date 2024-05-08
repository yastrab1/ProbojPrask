from unit import Unit, Melee, Ranged, Tank
from constants import Command, UnitType
from constants import *
from communicate import log

class Player:
    def __init__(self, name : str, spawn : int) -> None:
        self.name : str = name
        self.money : int = 0
        self.income_lvl : int = 0
        self.turret_lvl : int = 0
        self.turret : Unit = Unit(self.name, turret_hp, 0, turret_attack_chance[self.turret_lvl], turret_attack_range[self.turret_lvl], turret_dmg[self.turret_lvl], UnitType.TURRET)
        self.spawn : int = spawn
        self.upgrades: list[bool] = [False] * 3

    def tick_turn(self) -> None:
        self.money += income[self.income_lvl]

    def get_data(self, *additional) -> str:
        log(additional)
        return " ".join(map(str, (self.name, self.money, self.income_lvl, self.turret_lvl, *self.upgrades, *additional)))

    def make_action(self, action : int, hra: "Game"):
        match int(action):
            case Command.NONE.value:
                log("player action NONE " + self.name)
            case Command.INCOME.value:
                log("player action INCOME " + self.name)
                if self.income_lvl < len(income_cost) and self.money >= income_cost[self.income_lvl]:
                    self.money -= income_cost[self.income_lvl]
                    self.income_lvl += 1
                    log("Success")
                else:
                    log("Fail")
            case Command.TURRET.value:
                log("player action TURRET " + self.name)
                if self.turret_lvl < len(turret_cost) and self.money >= turret_cost[self.turret_lvl]:
                    self.money -= turret_cost[self.turret_lvl]
                    self.turret_lvl += 1
                    self.turret.attack_chance = turret_attack_chance[self.turret_lvl]
                    self.turret.attack_range = turret_attack_range[self.turret_lvl]
                    self.turret.attack_dmg = turret_dmg[self.turret_lvl]
                    log("Success")
                else:
                    log("Fail")
            case Command.MELEE.value:
                log("player action MELEE " + self.name)
                if self.money >= unit_cost[UnitType.MELEE.value] and hra.world[self.spawn] is None:
                    hra.world[self.spawn] = Melee(self.name, self.upgrades)
                    self.money -= unit_cost[UnitType.MELEE.value]
                    log("Success")
                else:
                    log("Fail")
            case Command.RANGED.value:
                log("player action RANGED " + self.name)
                if self.money >= unit_cost[UnitType.RANGED.value] and hra.world[self.spawn] is None:
                    hra.world[self.spawn] = Ranged(self.name, self.upgrades)
                    self.money -= unit_cost[UnitType.RANGED.value]
                    log("Success")
                else:
                    log("Fail")
            case Command.TANK.value:
                log("player action TANK " + self.name)
                if self.money >= unit_cost[UnitType.TANK.value] and hra.world[self.spawn] is None:
                    hra.world[self.spawn] = Tank(self.name, self.upgrades)
                    self.money -= unit_cost[UnitType.TANK.value]
                    log("Success")
                else:
                    log("Fail")
            case Command.HEALTH.value:
                log("player action HEALTH " + self.name)
                if not self.upgrades[Upgrade.HEALTH.value] and self.money >= unit_upgrade_cost:
                    self.upgrades[Upgrade.HEALTH.value] = True
                    log("Success")
                else:
                    log("Fail")
            case Command.ATTACK_CHANCE.value:
                log("player action ATTACK_CHANCE " + self.name)
                if not self.upgrades[Upgrade.ATTACK_CHANCE.value] and self.money >= unit_upgrade_cost:
                    self.upgrades[Upgrade.ATTACK_CHANCE.value] = True
                    log("Success")
                else:
                    log("Fail")
            case Command.ATTACK_DMG.value:
                log("player action ATTACK_DMG " + self.name)
                if not self.upgrades[Upgrade.ATTACK_DMG.value] and self.money >= unit_upgrade_cost:
                    self.upgrades[Upgrade.ATTACK_DMG.value] = True
                    log("Success")
                else:
                    log("Fail")
            case _:
                log(f"player action UNKNOWN ({action}) " + self.name)

    
