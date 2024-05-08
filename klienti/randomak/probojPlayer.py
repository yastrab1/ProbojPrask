import sys

from typing import Optional

from unit import Unit, UnitType
from constants import Command


class ProbojPlayer:
    """
    self.world je zoznam konstantnej dlzky (32), ktory obsahuje:
    - na krajoch Unit typu turret (domcek)
    - medzi nimi None alebo Unit
    """
    def __init__(self) -> None:
        self.name: str
        self.money: int
        self.income_lvl: int
        self.turret_lvl: int
        self.world: list[Optional[Unit]] = []
        self.upgrades: list[bool]

    def log(self, *args, **kwargs):
        """
        Vypíše dáta do logu. Syntax je rovnaká ako print().
        """
        print(*args, **kwargs, file=sys.stderr)

    def run(self) -> None:
        # hlavny cyklus hry

        while True:
            self.read_turn()
            turn: Command = self.make_turn()
            self.send_turn(str(turn.value))

    def make_turn(self) -> Command:
        # vrati aky tah chceme spravit

        raise NotImplementedError()

    def read_turn(self) -> None:
        self.name, money, income_lvl, turret_lvl, uh, uac, uad = input().split()
        self.upgrades = [uh, uac, uad]
        self.money, self.income_lvl, self.turret_lvl = map(
            int, (money, income_lvl, turret_lvl)
        )
        self.log("pla")
        x = input()
        self.world = []
        while x != ".":
            if x == "None":
                self.world.append(None)
            else:
                o, hp, mc, ac, ar, ad, t = x.split()
                hp, mc, ac, ar, ad, t = map(int, (hp, mc, ac, ar, ad, t))
                self.world.append(Unit(o, hp, mc, ac, ar, ad, UnitType(t)))
            x = input()

    def send_turn(self, turn: str) -> None:
        self.log(turn)
        print(turn)
        print(".", flush=True)
        self.log("Sent", turn)
