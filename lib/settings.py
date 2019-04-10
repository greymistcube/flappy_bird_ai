from lib.constants import TICKRATE

DIFFICULTY_SETTINGS = {
    "easy": {
        "wall_distance": 240,
    },
    "normal": {
        "wall_distance": 200,
    },
    "hard": {
        "wall_distance": 160,
    },
}

class Settings:
    def __init__(self, difficulty="normal", num_balls=1, multiplier=1):
        self.wall_distance = DIFFICULTY_SETTINGS[difficulty]["wall_distance"]
        self.num_balls = num_balls
        self.tickrate = TICKRATE * multiplier
        return

    def update(self, events):
        self.tickrate = TICKRATE * events.multiplier
        return

    def set_num_balls(self, num_balls):
        self.num_balls = num_balls
        return

    def set_tickrate(self, multiplier):
        self.tickrate = TICKRATE * multiplier
        return
