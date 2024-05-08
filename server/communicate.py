import sys
from typing import Optional


def printlines(*args):
    print(*args, sep="\n", flush=True)


def log(*args):
    pass
    print(*args, file=sys.stderr)


def read_config():
    header = input()
    assert header == "CONFIG", "didnt receive config"
    players = input().split()
    observe = input()
    foot = input()
    assert foot == ".", "Config did not end"
    return players, observe


def send_end() -> None:
    printlines("END", ".")


def to_observer(data: list[str]) -> None:
    printlines("TO OBSERVER", *data, ";", "", ".")
    answer = input()
    assert answer == "OK", "to Observer failed"
    while answer != ".":
        answer = input()


def set_scores(players: list[str], scores: list[int]) -> None:
    print("SCORES")
    for i in range(len(players)):
        print(f"{players[i]} {scores[i]}")
    print(".", flush=True)
    answer = input()
    assert answer == "OK", "set Scores failed"
    while answer != ".":
        answer = input()


def to_player(player: str, data: list[str]) -> None:
    printlines(f"TO PLAYER {player}", *data, ".")
    answer = input()
    if answer == "DIED":
        log(f"{player} DIED")
    elif answer == "ERROR":
        log("Error")
        data = []
        read = input()
        while read != ".":
            data.append(read)
            read = input()
    else:
        assert answer == "OK", "to Player failed"
    while answer != ".":
        answer = input()


def read_player(player: str) -> Optional[str]:
    printlines(f"READ PLAYER {player}", ".")
    answer = input()
    if answer == "DIED":
        log(f"{player} DIED")
        while answer != ".":
            answer = input()
        return "None"
    elif answer == "ERROR":
        log("Error")
        data = []
        read = input()
        while read != ".":
            data.append(read)
            read = input()
        return "None"
    else:
        assert answer == "OK", "to Player failed"
        data = []
        read = input()
        while read != ".":
            data.append(read)
            read = input()
        if len(data) != 1:
            log(f"{player} sent unexpected amount of data {len(data)}")
        return "None" if len(data) == 0 else data[0]


def kill_player(player: str) -> None:
    printlines(f"KILL PLAYER {player}", ".")
    answer = input()
    assert answer == "OK", "kill Player failed"
    while answer != ".":
        answer = input()
