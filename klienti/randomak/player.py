import random
from probojPlayer import ProbojPlayer
from constants import *

class MyPlayer(ProbojPlayer):
    def make_turn(self) -> Command:
        return random.choice(list(Command))
            


if __name__ == "__main__":
    p = MyPlayer()
    p.run()