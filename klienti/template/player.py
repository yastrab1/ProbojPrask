import math
import random
from probojPlayer import ProbojPlayer
from constants import *
class MyPlayer(ProbojPlayer):
    def __init__(self):
        super().__init__()
        self.turn = 0
        self.side = None
    def make_turn(self) -> Command:
        self.turn += 1
        if self.turn == 1:
            return Command.INCOME
        if self.turn <= 25:
            self.side = self.checkCurrentPlayer()
            return Command.BAGER
        self.log(str(self.side) + "side")
        return Command.BAGER
    def checkCurrentPlayer(self):
        if self.world[0]:
            if self.world[0].owner == self.name:
                return 0
        if self.world[30]:
            if self.world[30].owner == self.name:
                return 30
        return None
    def getThreat(self):
        threat = 0
        for i in range(len(self.world)):
            unit = self.world[i]
            if not unit:
                continue
            threatMultiplier = 1
            threatRaw = 0
            if unit.owner == self.name:
                threatMultiplier = -1
            if unit.type == UnitType.BAGER:
                threatRaw = 1
            if unit.type == UnitType.DVIHAK:
                threatRaw = 3
            if unit.type == UnitType.VALEC:
                threatRaw = 5
            distance = 1
            if self.side:
                distance = abs(self.side-i)
            threat += threatMultiplier * distance * threatRaw
        return threat
if __name__ == "__main__":
    p = MyPlayer()
    p.run()