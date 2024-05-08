import random
import time
import communicate
from communicate import log
from game import Game
from constants import max_turns, Command
from observer import Observer

def duration(start: float, end: float) -> float:
    return round((end - start) * 1000, 1)

def main():
    seed = int(time.time())
    # seed = 1714905184 # TEMP TODO
    random.seed(seed)
    log("seed is " + str(seed))

    players, observe = communicate.read_config()

    if observe == "observe":
        observe = True
        obs = Observer()

    hra = Game(players[0], players[1])

    # spravime zaznam na zaciatku
    data: list[str] = []
    data.extend([hra.p1.get_data(0), hra.p2.get_data(0)])
    data.extend(hra.observe())
    communicate.to_observer(data)
    if observe:
        obs.draw_turn(0, data)

    for turn in range(1, max_turns + 1):
        log("NEW TURN " + str(turn))
        # spravime tah

        actions = []

        start = time.time()

        # zistime tahy od hracov
        world = hra.get_data()
        for p in hra.p1, hra.p2:
            data: list[str] = [p.get_data()]
            data.extend(world)
            communicate.to_player(p.name, data)
            ans = communicate.read_player(p.name)
            actions.append(ans)
            end = time.time()
            log(f"{p.name} responded in {duration(start, end)}ms with {ans}")
            start = end
            world = world[::-1]

        # vykoname zmeny
        for i in range(len(players)):
            action = actions[i]
            try:
                log("try")
                int(action)
            except ValueError:
                log("except")
                log(f"{players[i]} send wrong command")
                action = Command.NONE.value
            [hra.p1, hra.p2][i].make_action(int(action), hra)

        # spravime tah - pridame peniaze, a odsimulujeme boj
        hra.tick_turn()

        # zaznamename
        data: list[str] = []
        data.extend([hra.p1.get_data(actions[0])])
        data.extend([hra.p2.get_data(actions[1])])
        data.extend(hra.observe())

        end = time.time()
        log(f"server done in {duration(start, end)}ms")
        start = end

        communicate.to_observer(data)
        if observe:
            obs.draw_turn(turn, data)

        end = time.time()
        log(f"observer done in {duration(start, end)}ms")
        start = end

        # zistime ci nemala skoncit hra
        for p in hra.p1, hra.p2:
            if p.turret.hp <= 0:
                game_end(hra)

    game_end(hra)


def game_end(hra: Game) -> None:
    log("GAME END")
    diff = max(0, hra.p1.turret.hp) - max(0, hra.p2.turret.hp)
    scores = [diff + 2000 if hra.p2.turret.hp <= 0 else 0,
    -diff + 2000 if hra.p1.turret.hp <= 0 else 0]
    communicate.to_observer(["end"])
    communicate.set_scores([hra.p1.name, hra.p2.name], scores)
    communicate.send_end()


if __name__ == "__main__":
    main()
