# from lib.core import TICKRATE

TICKRATE = 60

class Settings:
    def __init__(self, num_balls=1, multiplier=1):
        self.num_balls = num_balls
        self.tickrate = TICKRATE * multiplier

    def update(self, events):
        if events.multiplier is not None:
            self.tickrate = TICKRATE * events.multiplier

    def set_num_balls(self, num_balls):
        self.num_balls = num_balls

    def set_tickrate(self, multiplier):
        if multiplier is not None:
            self.tickrate = TICKRATE * multiplier
