# Pyxel Knights

A game

## How to play the game

### What you will need

- Pyxel
- That's it

If you use the .exe / .html file, there is no need for Pyxel

If you want to play with friends, use [Parsec](https://parsec.app/)

You start with 110 Gold. You gain 10 coins each round + 10 for each farm.

IMPORTANT : If you loose vision of a unit, you cannot control it.

## How to build the game

- Download the source files or do a `git clone https://github.com/TRNEEDANAME/NDC-2023/` and unzip the .zip file
- Do a `cd PATH/TO/FOLDER`
- Then do `pyxel package  PATH/TO/FOLDER PYTHON_APP.py`
- If you want an exe or HTML file, do `pyxel app2exe FOLDER_NAME` or `pyxel app2html FOLDER_NAME`
- Package the app using 7 zip or the command line
- Voilà ! A new .exe / .html file is now ready !

## FAQ

### What are the controls ?

left, down, up, right : move the cursor

on empty tile:
1: tower = 50 gold
2: wall = 100 gold
3: casern = 70 gold
4: farm = 30 gold (+25% of cost for each subsequent farms)

on own caserne:
1: knight = 10 gold
2: archer = 30 gold
3: scout = 30 gold

on own unit:
1: move 
2: select for attack
3: attack

If you wish to fork the game, credit "TRNEEDANAME", "1Dorian" and "maybenotyou".

Coding : 1Dorian, maybenotyou
Ideas / brainstorming : TRNEEDANAME, maybenotyou, 1Dorian
Art : TRNEEDANAME, maybenotyou
Sound design : 1Dorian, maybenotyou
Documentation : TRNEEDANAME

This game was created for the [Nuit du Code](https://www.nuitducode.net/) which is a Game Jam where you have 6h to create an entire game from scratch using [Pyxel](https://github.com/kitao/pyxel), a free Python game librairy used to create retro-style games.
