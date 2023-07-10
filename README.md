# Spaceship Battle Game

## Overview
Spaceship Battle Game is an engaging 2D multiplayer game built with Python and Pygame. The goal is to control a spaceship and shoot down your opponent's spaceship while avoiding incoming bullets. The game is over when a player's health depletes, and the other player is declared the winner.

## Game Mechanics
- Each player starts with a health score of 10.
- Players can move their spaceship up, down, left, and right using the arrow keys (for Player 2) and the W, A, S, D keys (for Player 1).
- Each player can shoot bullets by pressing the control key. Player 1 uses the left control key, while Player 2 uses the right control key.
- When a bullet hits a spaceship, the health of the spaceship's player decreases by 1.
- The game ends when a player's health reaches 0. The other player is then declared the winner.

## Installation
You will need Python and Pygame to run this game. If you don't have Python installed, download and install it from [python.org](https://www.python.org/). After installing Python, you can install Pygame by running `pip install pygame` in your terminal.

## Running the Game
To run the game, navigate to the directory containing the game files in your terminal and run the command `python main.py`.

## Game Controls

For Player 1:
- Move up: W
- Move down: S
- Move left: A
- Move right: D
- Shoot: Left Control

For Player 2:
- Move up: Up arrow
- Move down: Down arrow
- Move left: Left arrow
- Move right: Right arrow
- Shoot: Right Control

## Assets
The game uses several assets including images and sounds to create a rich and engaging gaming experience. These assets are all located in the `Assets` directory.
