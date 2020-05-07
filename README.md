# Game "Space Invaders"

Version 1.3
Developer Rogov Artemy (artemiyrogov1@gmail.com)

## Description

This app is an implementation of the game SPACE INVADERS with acceleration of free fall and the player is in some type of "pit".

## Requirements

* `PyQT5` (installing by pip)

## Structure

Main file (GUI and implementation of the game): `SpaceInvaders.py`

Modules: `Enemies.py`, `Values`, `Levels.py`

Tests: `tests.py`

## How to play
for example you have levels: `level1.txt`, `level2.txt`
this way
`python SpaceInvader.py 2 1`
you will play at first `level2.txt`, after `level1.txt`

### Controlling

* `Key left`, `Key right` -- To control cart

* `Space` -- To fire

* `P` -- To pause the game

#### Details of implementation

`Enemies.py` contains information about all classes using in this game (invaders, bullets, cart, etc.)

`Values.py` contains all the constants using in this game

`Levels.py` parses information about levels from text files

You can make your own levels. You should only build new level`number`.txt using next sample:

		[easyinvader]
		damage = <value> (from 0 to infinity :) )
		lives = <value> (from 0 to infinity :) )
		type = <value> (from 1 to 3; 1 - aim on cart, 2 - aim near cart, 3 - random aim)

		[mediuminvader]
		damage = <value>
		lives = <value>
		type = <value>

		[hardinvader]
		damage = <value>
		lives = <value>
		type = <value>

		[enemies]
		<easyinvader> = <count>
		<mediuminvader> = <count>
		<hardinvader> = <count> (please don`t make more than summary 27 enemies, also it should be bigger than 0)

		[level]
		weight_cart = <value> (from 1 to 20, if it is very small, you will be very light, if it is very big, you won`t have opportunity to normally move)
		angle_cart = <value> (from 30 to 150)
		interval_cart = <value> (in ms, value=1000 - interval is 1 second)
		lives_cart = <value> (from 1 to infinity :) )
