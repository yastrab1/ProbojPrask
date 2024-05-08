from typing import Optional
from random import randint

from constants import *
from communicate import log
from player import Player
from unit import Unit


class Game:
    def __init__(self, p1: str, p2: str):
        self.p1: Player = Player(p1, 1)
        self.p2: Player = Player(p2, map_size)
        # self.p2.money = sum(income_cost) + sum(turret_cost)
        # for i in range(1):
        #     self.p2.make_action(Command.INCOME.value, self)
        # for i in range(5):
        #     self.p2.make_action(Command.TURRET.value, self)
        self.p1.money, self.p2.money = start_money, start_money
        self.world: list[Optional[Unit]] = [None for _ in range(map_size + 2)]
        self.world[0] = self.p1.turret
        self.world[-1] = self.p2.turret

    def tick_turn(self) -> None:
        self.p1.tick_turn()
        self.p2.tick_turn()

        self.had_action = [False] * len(self.world)
        self.attack()
        self.move_units()

    def move_units(self) -> None:
        def move_p2():
            for i in range(len(self.world)):
                if self.world[i] is None or self.had_action[i]:
                    continue
                if self.world[i].owner == self.p2.name:
                    if self.world[i].move() and self.world[i - 1] is None:
                        self.world[i], self.world[i - 1] = (
                            self.world[i - 1],
                            self.world[i],
                        )

        def move_p1():
            for i in range(len(self.world) - 1, 0, -1):
                if self.world[i] is None or self.had_action[i]:
                    continue
                if self.world[i].owner == self.p1.name:
                    if self.world[i].move() and self.world[i + 1] is None:
                        self.world[i], self.world[i + 1] = (
                            self.world[i + 1],
                            self.world[i],
                        )

        if randint(0, 1):
            move_p1()
            move_p2()
        else:
            move_p2()
            move_p1()

    def attack(self) -> None:
        for i in range(len(self.world)):
            this_unit = self.world[i]
            if this_unit is None:
                continue
            targets = (
                self.world[i + 1 : i + 1 + this_unit.attack_range]
                if this_unit.owner == self.p1.name
                else self.world[max(0, i - this_unit.attack_range) : i][::-1]
            )
            log(i, targets, self.world)
            ally_next_to_me = targets[0] is not None and targets[0].owner == this_unit.owner
            ally_in_front_of_me = False
            for target_unit in targets:
                if target_unit is None:
                    continue
                if target_unit.owner == this_unit.owner:
                    ally_in_front_of_me = True
                else:
                    if ally_next_to_me or not ally_in_front_of_me:
                        self.had_action[i] = True
                        if this_unit.attack(): # Note: maybe won't attack
                            target_unit.hp -= this_unit.attack_dmg
                    break

        # zrusime mrtve jednotky - nie turret
        for i in range(1, len(self.world) - 1):
            if self.world[i] is None:
                continue
            if self.world[i].hp <= 0:
                self.world[i] = None

    def get_data(self) -> list[str]:
        return ["None" if u is None else u.get_data() for u in self.world]

    def observe(self) -> list[str]:
        return ["None" if u is None else u.observe() for u in self.world]
