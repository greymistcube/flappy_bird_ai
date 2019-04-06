# from lib.core import TICKRATE

TICKRATE = 60

class Settings:
    def __init__(self, num_balls=1, tickrate=TICKRATE):
        self.num_balls = num_balls
        self.tickrate = tickrate

    def set_num_balls(self, num_balls):
        self.num_balls = num_balls

    def set_tickrate(self, multiplier):
        if multiplier is not None:
            self.tickrate = self.tickrate * multiplier

    def update(self, events):
        if events.multiplier is not None:
            self.tickrate = self.tickrate * events.multiplier
