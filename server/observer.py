import gzip
import sys
import tkinter as tk
from tkinter import font
import time
from images import img1, img2

from pynput.keyboard import Listener

from constants import *
from communicate import log
import base64

IMAGE_PATH = "../../server/images/"
class Observer:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("proboj")
        self.canv = tk.Canvas(self.root, height=500, width=1024, bg='dimgray')
        '''self.canv.create_text(10, 10, text=players[0], anchor=tk.NW)
        self.canv.create_text(990, 10, text=players[1], anchor=tk.NE)'''
        self.canv.pack()
        self.imgs = [[tk.PhotoImage(data=file) for file in img1],
                     [tk.PhotoImage(data=file) for file in img2]]
        self.last_draw : float = time.time()
        self.speed : int = 4
        self.wait : list[float] = [1, 0.4, 0.2, 0.1, 0.05, 0.025, 0.012, 0.006, 0]

        Listener(on_press=self.change_speed).start()

        default_font = font.nametofont("TkDefaultFont")
        default_font.configure(size=18)
        self.root.update()


    def change_speed(self, key):
        speeds = {str(i+1): i for i in range(len(self.wait))}
        if hasattr(key, 'char'):
            if key.char in speeds:
                self.speed = speeds[key.char]
        

    def draw_turn(self, turn : int, data : list[str]):
        new_frame = self.last_draw + self.wait[self.speed]
        if time.time() < new_frame:
            wait = max(0, new_frame - time.time())
            log(f"waiting {wait * 1000} ms")
            time.sleep(wait)
        self.last_draw = time.time()

        self.canv.delete("all")

        speed = ["1/20x", "1/8x", "1/4x", "1/2x", "1x", "2x", "4x", "8x", "max"][self.speed]
        self.canv.create_text(2, 2, anchor=tk.NW, text=f"cur speed: {speed} (zmen klavesou 1-9)")

        self.canv.create_text(512, 30, text="turn " + str(turn))

        # dashed line down the quarters
        IMG_SIZE = 32
        self.canv.create_line(512, 250, 512, 400, fill='black', dash=(4, 8))
        for dist in (2, 5, 8, 11):
            x = (dist + 1) * IMG_SIZE
            self.canv.create_line(x, 250, x, 400, fill='black', dash=(4, 16))
            x = 1024 - (dist + 1) * IMG_SIZE
            self.canv.create_line(x, 250, x, 400, fill='black', dash=(4, 16))


        h: int = 30
        def draw_side(name: str, money: str, income_lvl, turret_lvl, uh: str, uac: str, uad: str,action: str, key_income: str, key_turret: str, key_uh: str, key_uac: str, key_uad: str, x: int, anchor):
            income_lvl, turret_lvl = int(income_lvl), int(turret_lvl)
            self.canv.create_text(x, h * 2, text=f"{name} {uh} ({key_uh}) {uac} ({key_uac}) {uad} ({key_uad})", anchor=anchor)
            upgrade_cost = str(income_cost[income_lvl]) if income_lvl < len(income_cost) else "max level"
            self.canv.create_text(x, h * 3, text=f"{money} + {income[income_lvl]} ({key_income}) : {upgrade_cost}", anchor=anchor, fill="gold")
            upgrade_cost = str(turret_cost[turret_lvl]) if turret_lvl < len(turret_cost) else "max level"
            self.canv.create_text(x, h * 4, text=f"{turret_lvl} ({key_turret}) : {upgrade_cost}", anchor=anchor, fill="gray")
            action = Command(int(action)).name if action != "None" else Command.NONE.name
            self.canv.create_text(x, h * 5, text=action, anchor=anchor)

        log(data)
        draw_side(*data[0].split(), "Q", "A", "E", "D", "C", 10, tk.NW)
        draw_side(*data[1].split(), "P", "L", "I", "J", "N", 1014, tk.NE)

        btns = [
            ["", " (W)", " (S)", " (X)"],
            ["", " (O)", " (K)", " (M)"]
        ]

        for i in range(1, 4):
            y = h * 5 + i * IMG_SIZE
            self.canv.create_image(40, y, anchor=tk.NE, image=self.imgs[0][i])
            self.canv.create_image(980, y, anchor=tk.NW, image=self.imgs[1][i])
            self.canv.create_text(50, y, anchor=tk.NW, text=str(unit_cost[i]) + btns[0][i])
            self.canv.create_text(970, y, anchor=tk.NE, text=str(unit_cost[i]) + btns[1][i])


        player2_name = data[1].split()[0]
        y = 300
        for i in range(2, len(data)):
            if data[i] == "None":
                continue
            o, h, m, t = data[i].split()
            h, m, t = int(h), int(m), int(t)
            x = (i-2)*IMG_SIZE
            self.canv.create_image(x, y, anchor=tk.NW, image=self.imgs[o == player2_name][t])
            self.canv.create_rectangle(x, y, x + IMG_SIZE, y + 4, fill='gray')
            self.canv.create_rectangle(x, y, x + IMG_SIZE*h//m, y + 4, fill='green')

        self.root.update()

def observe_file(file : str):
    f =  gzip.open(file, 'r')
    x = f.readline().decode()[:-1]
    o = Observer()
    turn = 0
    while x != "end":
        data = []
        while x != ';':
            data.append(x)
            x = f.readline().decode()[:-1]
        o.draw_turn(turn, data)
        turn += 1
        x = f.readline().decode()[:-1]




if __name__ == "__main__":
    observe_file(sys.argv[1])