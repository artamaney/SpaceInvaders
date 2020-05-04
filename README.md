# Game "Space Invaders"

Version 1.1
Developer Rogov Artemy (artemiyrogov1@gmail.com)

## Description

This app is an implementation of the game SPACE INVADERS with acceleration of free fall and the player is in some type of "pit".

## Requirements

* `PyQT5` (installing by pip)

## Structure

Main file (GUI and implementation of the game): `SpaceInvaders.py`

Modules: `Enemies.py`, `Values`, `Levels.py`

Tests: `tests.py`

### Controlling

* `Key left`, `Key right` -- To control cart

* `Space` -- To fire

#### Details of implementation

`Enemies.py` contains information about all classes using in this game (invaders, bullets, cart, etc.)

`Values.py` contains all the constants using in this game

`Levels.py` parses information about levels from text files and passes them into the `Value.py` module

You can make your own levels. You should only build new level`number`.txt using next sample:

		easyInvadersCount=18
		mediumInvadersCount=0
		hardInvadersCount=0 (don`t make more than 24 invaders)
		interval=2000 (it should be more than 0)
		type=1 (1 - Aim on cart, 2 - Aim on cart + inaccuracy, 3 - random aim)
		bunkersCount=3 (it should be from 0 to 5)
