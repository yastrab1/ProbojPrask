import random
from typing import Optional

from constants import *
from probojPlayer import ProbojPlayer
from unit import Unit

INF = 10**9 - 1
MIN_SAFE_DIST = 1
UPGRADE_FORMATION = [(0, 0), (1, 0), (1, 1), (2, 1), (2, 2), (3, 2)] # NOT USED
ATTACK_FORMATION = [(0,)] * 5 + [(0, 1)] * 5 + [(2, 1, 2, 1, 1)] * 100
DESIRED_LEVEL_INCOME = 3
DESIRED_LEVEL_TURRET = 2
BAGER_SAFETY_NET = unit_cost[UnitType.BAGER.value] // 2
ID_TO_UNIT = [UnitType.BAGER, UnitType.DVIHAK, UnitType.VALEC]
ID_TO_COMMAND = [Command.BAGER, Command.DVIHAK, Command.VALEC]

debug_file = open("mudry.debug", "w")
def debug(*args):
    debug_file.write(" ".join(map(str, args)) + "\n")
    debug_file.flush()

class Mudry(ProbojPlayer):
    # self.name: str
    # self.money: int
    # self.income_lvl: int
    # self.turret_lvl: int
    # self.world: list[Optional[Unit]] = []
    moje_jednotky: list[tuple[int, Unit]]
    jeho_jednotky: list[tuple[int, Unit]]
    buy_queue = []
    attack_stage = 0

    """
    Strategie:
    - nechceme aby sa dotykal nasho domceka -> bager
    - chceme setrit peniaze tym, ze pouzivame pasivnu obranu
    - treba si davat pozor na dvihak utok (udrziavat ho dostatocne daleko)
    - chceme zarabat viac ako on
    - poradie upgradovania je income -> defense -> income -> defense -> ...
    - utocime vo formacii valec valec dvihak
    - nemam dost penazi aby som kupoval ako chcem, takze posielam vo vlnach
    """

    def zivoty_jednotiek(self):
        self.log(self.moje_jednotky, self.jeho_jednotky)

        def sucet(jednotky):
            return sum(jednotka.hp for _, jednotka in jednotky)

        return sucet(self.moje_jednotky), sucet(self.jeho_jednotky)

    def kolko_kol_protivnik_pride_k_nasemu_domceku(self):
        hp_moje, hp_jeho = self.zivoty_jednotiek()
        if hp_jeho == 0:
            return INF
        vzdialenost = min(i - u.attack_range for i, u in self.jeho_jednotky)
        maximalny_utok = max(unit_attack_dmg)
        cas = hp_moje / maximalny_utok + vzdialenost
        debug(
            "kolko_kol",
            hp_moje,
            hp_jeho,
            vzdialenost,
            maximalny_utok,
            cas,
        )
        return cas

    def kolko_mozem_minut_bez_ohrozenia_domceka(self):
        cas = self.kolko_kol_protivnik_pride_k_nasemu_domceku()
        if cas == INF:
            return INF
        if cas <= MIN_SAFE_DIST:
            return -1
        debug("kolko_mozem", cas, self.money, self.income_lvl)
        peniaze = self.money + income[self.income_lvl] * cas
        mozem_minut = max(0, peniaze - unit_cost[UnitType.BAGER.value])
        return mozem_minut

    def make_turn(self) -> Command:
        """
        Toto je funkcia ktoru zavola server ked sme na tahu.
        Budeme mat vtedy nastavene vsetky atributy hraca a sveta.
        Mozeme tu robit co chceme, volat ine funkcie, pisat si debugovacie vypisy, ...
        ale na konci musime vratit nejaky prikaz.
        """
        self.log("jeeej", self.name, self.money, self.income_lvl, self.turret_lvl)
        self.log(self.world)

        # return Command.BAGER

        # # risky strategy
        # if self.income_lvl == 0:
        #     return Command.INCOME

        self.moje_jednotky = []
        self.jeho_jednotky = []
        for i in range(1, len(self.world) - 1):
            jednotka = self.world[i]
            if jednotka is None:
                continue
            if jednotka.owner == self.name:
                self.moje_jednotky.append((i, jednotka))
            else:
                self.jeho_jednotky.append((i, jednotka))


        # nikdy nemozeme byt pozadu na income
        # tipneme si, ze zaraba vela ak ma vela penazi na ploche
        jeho_cena = sum(unit_cost[unit.type.value] for _, unit in self.jeho_jednotky if unit is not None)
        absurdne_hodnoty = [inc * 120 for inc in income]
        absurdne_hodnoty[-1] = INF
        if jeho_cena > absurdne_hodnoty[self.income_lvl] and self.world[0].hp > turret_hp * 0.3:
            return Command.INCOME


        # dotyka_sa = self.world[1] is not None and self.world[1].owner != self.name
        # if dotyka_sa and self.turret_lvl == 0:
        #     return Command.TURRET

        mozem_minut = self.kolko_mozem_minut_bez_ohrozenia_domceka()
        if mozem_minut >= 0:
            mozem_minut = max(0, mozem_minut - BAGER_SAFETY_NET)
        debug("mozem_minut", mozem_minut, self.money)
        if mozem_minut == -1 and self.money >= unit_cost[UnitType.BAGER.value]:
            if self.money >= unit_cost[UnitType.VALEC.value]:
                return Command.VALEC
            return Command.BAGER

        *can_buy_unit, can_buy_income, can_buy_turret = [
            mozem_minut >= cost and self.money >= cost
            for cost in (
                unit_cost[UnitType.BAGER.value],
                unit_cost[UnitType.DVIHAK.value],
                unit_cost[UnitType.VALEC.value],
                income_cost[self.income_lvl]
                if self.income_lvl < len(income_cost)
                else INF,
                turret_cost[self.turret_lvl]
                if self.turret_lvl < len(turret_cost)
                else INF,
            )
        ]
        can_buy_attack = self.world[1] is None

        if can_buy_income and self.income_lvl < DESIRED_LEVEL_INCOME and self.income_lvl <= self.turret_lvl:
            return Command.INCOME
        if can_buy_turret and self.turret_lvl < min(self.income_lvl, DESIRED_LEVEL_TURRET):
            return Command.TURRET
        if self.income_lvl == DESIRED_LEVEL_INCOME and self.turret_lvl == DESIRED_LEVEL_TURRET:
            if can_buy_attack:
                if not self.buy_queue:
                    buy = (
                        ATTACK_FORMATION[self.attack_stage]
                        if self.attack_stage < len(ATTACK_FORMATION)
                        else (random.randint(0, 2),)
                    )
                    if sum(unit_cost[ID_TO_UNIT[b].value] for b in buy) <= self.money:
                        self.buy_queue = list(buy)
                        self.attack_stage += 1
                if self.buy_queue:
                    unit_val = self.buy_queue[0]
                    if self.money >= unit_cost[unit_val]:
                        self.buy_queue.pop(0)
                        return ID_TO_COMMAND[unit_val]
        return Command.NONE


if __name__ == "__main__":
    p = Mudry()
    p.run()
