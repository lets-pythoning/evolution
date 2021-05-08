# Evolution

> This program is a simulation of the board game *Evolution*. **It is completed, and not very stable!**, it had undergone two reconstructions and countless debugs.

---

It completes the entire card system by inheriting the Card abstract base class, and implements the player through the Player class. The state in the program is a global variable that stores all game data, and its structure cannot be changed casually.

**game_utils.py** is the base of **enter.py**, **enter.py** implement the game flow overall, **constants.py** save all constants, if you want to easily customize the game, please change the constants in **constants.py**.

---

- python: 3.6.6
- package_used: random, os, time, typing, sys, json
- author: https://github.com/lets-pythoning
- repositories: https://github.com/lets-pythoning/evolution
