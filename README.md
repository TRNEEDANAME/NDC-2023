# Pyxel Knights

A game

## How to play the game

### What you will need

- Pyxel
- That's it

If you use the .exe file, there is no need for Pyxel

If you want to play with friends, use [Parsec](https://parsec.app/)

You start with 110 Gold. You gain 10 coins each round + 10 for each farm.

IMPORTANT : If you loose vision of a unit, you cannot control it.

## How to build the game

- Use a terminal (works on all OS)
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
