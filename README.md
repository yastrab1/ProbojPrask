hracia plocha:

- ma 32 policok
- na koncoch mame domceky
- z domcekov si vieme kupovat a teda generovat vozidla
- na kazdom policku vie byt najviac jedna utocna jednotka

existuju upgrady:

- turret
- income
- unit health
- unit attack chance
- unit attack damage

existuju jednotky:

- bager
- dvihak
- valec

kola:

- hra trva 5000 kol
- kazde kolo sa generuje peniaze podla levelu incomu
- kazde kolo viem vykonat jednu akciu -- kupa jednotky alebo upgrade
- ak je policko priamo pred domcekom obsadene tak kupa jednotky zlyha
- podobne ak nemam dost penazi na danu akciu alebo uz mam maximalny level upgradu tak akcia zlyha
- ak akcia zlyha tak sa nic nestane
- pre kazde kolo sa nahodne urci kto zacina
- najprv sa pokusia pohnut vsetky jednotky zacinajuceho hraca, potom toho druheho

utocne jednotky sa spravaju nasledovne:

- najprv sa pokusia zautocit, ak maju pred sebou nepriatela
- inak sa pokusia pohnut dopredu
- vsimnite si, ze pokus o zautocenie moze zlyhat a v tom pripade sa tak ci tak nehybeme dopredu
- pokus o pohyb a utok ma sancu na uspech, ak neuspeje tak sa jednoducho nevykona
- kazda jednotka zomiera az na konci kola, teda ak mala zautocit alebo sa pohnut tak to vzdy stihne vykonat

dvihak je specialny:

- ked pred sebou vidi kamarata, tak sa snazi ist dopredu
- ked pred sebou vidi nepriatela, tak stoji a snazi sa utocit
- ked pred sebou vidi kamarata, ale nevie sa uz pohnut, snazi sa utocit

domovska zakladna ma:

- 2000 zivota
- zivot sa nikdy neregeneruje
- uz od zaciatku vie davat utok do malej vzdialenosti

bodovanie je nasledovne:

- hrac dostane pocet bodov rovny rozdielu zivotov zakladni
- ak sa vitazovy podari protihraca zabit, ziska navyse 2000 bodov
- ak teda napriklad bez straty zivota zabijem protihraca, ziskam 4000 bodov a protihrac -2000

Instalacia:

- Stiahni zip z proboj.sus.3sten.sk
- potrebujete:
  - python
  - tkinter, pynput - da sa stiahnut cez pip

Spustanie:

- example/config.json - popis ako sa maju spustat jednotlivy hraci
- example/games.json - popis ake hry sa maju spustit
- linux: `./runner example/config.json example/games.json`
- windows:
- treba v `example/config_win.json` prepisat USER tak aby sedela cesta k pythonu
- `runner.exe example/config_win.json example/games`
- ked si chcete pustit hru znovu `python server/observer.py CESTA-KU-HRE/observer.gz`

Programovanie:

- implementujeme funkciu make_turn
- self.name: str - naše meno
- self.money: int - naše peniaze
- self.income_lvl: int - náš level príjmu
- self.turret_lvl: int - náš level domčeku
- self.world: list[Optional[Unit]] - Jednotky ktoré sú na mape
- self.upgrades: list[bool] - naše upgrady
- Dôležité hodnoty sú v constants
