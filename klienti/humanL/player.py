import sys
from pynput.keyboard import Listener, Key



class humanPlayerLeft:
    def __init__(self) -> None:
        self.sent = 0
        self.read = 0

    def log(self, *args):
        """
        Vypíše dáta do logu. Syntax je rovnaká ako print().
        """
        print(*args, file=sys.stderr)

    def run(self) -> None:
        # hlavny cyklus hry

        while True:
            self.readTurn()
            self.log("read")
            self.read += 1
            if self.read > self.sent:
                self.sent += 1
                self.sendTurn("0")
    
    def makeTurn(self, key) -> None:
        self.log("make turn")
        # vrati aky tah chceme spravit

        if hasattr(key, 'char'):
            match key.char:
                case 'q':
                    self.sent += 1
                    self.sendTurn("1")
                case 'a':
                    self.sent += 1
                    self.sendTurn("2")
                case 'w':
                    self.sent += 1
                    self.sendTurn("3")
                case 's':
                    self.sent += 1
                    self.sendTurn("4")
                case 'x':
                    self.sent += 1
                    self.sendTurn("5")
                case 'e':
                    self.sent += 1
                    self.sendTurn("6")
                case 'd':
                    self.sent += 1
                    self.sendTurn("7")
                case 'c':
                    self.sent += 1
                    self.sendTurn("8")

        

    def readTurn(self) -> None:
        input()
        x = input()
        while x != ".":
            x = input()



    def sendTurn(self, turn : str) -> None:
        self.log(turn)
        print(turn)
        print(".", flush=True)
        self.log("Sent")

if __name__ == "__main__":
    p = humanPlayerLeft()
    l = Listener(on_press=p.makeTurn)
    l.start()

    p.run()

