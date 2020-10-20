# Game "Space Invaders"

Version 2.1
Developer Rogov Artemy (artemiyrogov1@gmail.com)

## Description

This app is an implementation of the game SPACE INVADERS with acceleration of free fall and the player is in some type of "pit".

## Requirements

* `PyQT5` (installing by pip)

## Structure

Main module (GUI and implementation of the game): `SpaceInvaders.py`

Modules: `Enemies.py`, `Values.py`, `Levels.py`, `Images.py`

Tests: `test_Enemies.py`

## How to play
for example you have levels: `level1.txt`, `level2.txt`
using command line you can run the game

`python SpaceInvaders.py --name YOURNAME level2.txt level1.txt`


you will play at first `level2.txt`, after `level1.txt` and your name in scoreboard will be YOURNAME. If you don`t use --name the name in scoreboard will be user

### Controlling

* `Key left`, `Key right` - To control cart

* `Space` - To fire

* `P` - To pause the game

* `S` - To save the game

* `V` - To load the last saving

* `O` - To see a scoreboard during a game (pause_mode activating automatically)

#### Details of implementation

`Enemies.py` contains information about all classes using in this game (invaders, bullets, cart, etc.)

`Values.py` contains all the constants using in this game

`Levels.py` parses information about levels from text files

`Images.py` contains all images ^-^


You can make your own levels. You should only build new level`name`.txt using next sample:

		[enemy.name]
		damage = value (from 0 to infinity :) )
		lives = value (from 0 to infinity :) )
		type = value (from 1 to 3; 1 - aim on cart, 2 - aim near cart, 3 - random aim)

		[enemy.name1]
		damage = value
		lives = value
		type = value

		[enemy.name2]
		damage = value
		lives = value
		type = value
		
		[bonus1]
		type = value (bullet or health)
		probability = value (0 - 100)
		force = value (0-5) - only if type is bullet
		health = value (0-5) - only if type is health

		[level]
		weight_cart = value (from 5 to 15)
            interval_cart = value (from 1000 to 10000)
            lives_cart = value (from 1 to 10)
            interval_mystery_ship = value (from 5000 to 500000)
            mystery_ship_score = value (from 0 to 5000)
            fire_score = value (from 0 to 250)