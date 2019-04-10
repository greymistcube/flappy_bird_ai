# Flappy Bird Clone with NEAT

![Game Screen](./docs/img/peek.gif)

You can checkout out for more details about this project on
[this github page.](https://greymistcube.github.io/flappy_bird_ai/)

## Dependencies

This project requires `numpy` and `pygame` packages to run.
```
pip install numpy
pip install pygame
```
Versions `1.16.2` and `1.9.4` were used respectively during the devlopment.

## Usage

Run with
```
python game.py
```
to run the game normally in a human playable mode with default settings.
Various other options may be given at startup. For example,
```
python game.py -z 3 -d hard -n 200 neat
```
will start the game with 3x zoom, difficulty set to hard, and 200 birds
per generation for NEAT AI. More help on the usage can be found
with `-h` option.
