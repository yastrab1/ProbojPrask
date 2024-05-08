import random
from probojPlayer import ProbojPlayer
from constants import *
from server.constants import Command


class MyPlayer(ProbojPlayer):
    def make_turn(self) -> Command:
        return Command.BAGER
        
        


if __name__ == "__main__":
    p = MyPlayer()
    p.run()