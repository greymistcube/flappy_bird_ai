from lib.constants import TICKRATE

DIFFICULTY_SETTINGS = {
    "easy": {
        "wall_distance": 240,
        "jump_velocity": -3.2,
    },
    "normal": {
        "wall_distance": 200,
        "jump_velocity": -3.6,
    },
    "hard": {
        "wall_distance": 160,
        "jump_velocity": -4.0,
    },
}

class Settings:
    _instance = None

    # implementing this class as singleton
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    # this should be called at least once with args in main.py
    def __init__(self, args=None):
        if args is not None:
            self.tickrate = TICKRATE
            self.wall_distance = DIFFICULTY_SETTINGS[args.d]["wall_distance"]
            self.jump_velocity = DIFFICULTY_SETTINGS[args.d]["jump_velocity"]
            self.num_balls = args.n
        return

    def event_update(self, events):
        self.tickrate = TICKRATE * events.multiplier
        return

