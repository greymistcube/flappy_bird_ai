import sys
import random
import pygame

import constants as const

def load_image(file):
    image = pygame.image.load(file)
    return image

class Ball:
    image = load_image("blue_ball.png")

    def __init__(self):
        self.rect = self.image.get_rect()
        self.x, self.y = const.START_POSITION
        self.rect.center = (self.x, self.y)
        self.velocity = 0
        self.score = 0
        return
    
    def move(self):
        self.rect = self.rect.move((0, self.velocity))
        self.y = self.y + self.velocity
        return
    
    def accelerate(self):
        self.velocity = self.velocity + const.GRAVITY
        return
    
    def jump(self):
        self.velocity = const.JUMP_VELOCITY
    
    def out_of_bounds(self):
        return (self.rect.top < 0) or (self.rect.bottom > const.HEIGHT)

class Wall:
    image = load_image("brick_wall.png")

    # here, (x, y) correspond to the center of a wall
    def __init__(self, x, y):
        self.lower = self.image.get_rect()
        self.upper = self.image.get_rect()
        y_offset = (const.HOLE_SIZE + self.image.get_height()) // 2
        self.lower.center = (x, y + y_offset)
        self.upper.center = (x, y - y_offset)
        self.x = x
        self.y = y
        self.speed = const.MOVE_SPEED
        return
    
    def move(self):
        self.lower = self.lower.move((self.speed, 0))
        self.upper = self.upper.move((self.speed, 0))
        self.x = self.x + self.speed
        return
    
    def out_of_bounds(self):
        return self.lower.right < 0

class GameEnvironment:
    def __init__(self):
        self.walls = []
        self.surface = pygame.Surface(const.SIZE)
        return
    
    def add_ball(self):
        self.ball = Ball()
        return
    
    def add_wall(self):
        # if no wall exists, add one at the right end of the screen
        # otherwise, add one some distance away from the right-most one
        if not self.walls:
            x = const.WIDTH
        else:
            x = self.walls[-1].x + const.WALL_DISTANCE

        variance = random.randint(-const.Y_VARIANCE, const.Y_VARIANCE)
        y = (const.HEIGHT // 2) + variance

        self.walls.append(Wall(x, y))
        return
    
    def remove_wall(self):
        self.walls.pop(0)
        return
    
    def update(self, pressed_keys):
        # move game objects
        self.ball.move()
        self.ball.accelerate()
        for wall in self.walls:
            wall.move()

        # remove a wall if it gets past the screen and add in a new one
        if self.walls[0].out_of_bounds():
            self.remove_wall()
            self.add_wall()
        
        if pressed_keys[pygame.K_SPACE]:
            self.ball.jump()

        return
    
    def check_game_over(self):
        return self.ball.out_of_bounds() or collision(self)
    
    def draw(self):
        self.surface.fill(const.WHITE)
        self.surface.blit(self.ball.image, self.ball.rect)
        for wall in self.walls:
            self.surface.blit(wall.image, wall.lower)
            self.surface.blit(wall.image, wall.upper)
        text = font.render("Score: " + str(self.ball.score), True, const.BLACK)
        self.surface.blit(text, (0, 0))
        return self.surface


def new_game():
    env = GameEnvironment()
    env.add_ball()
    for _ in range(5):
        env.add_wall()

    return env

def collision(env):
    ball = env.ball
    wall = env.walls[0]

    # for the current setup, we only need to check with the first wall
    if ball.rect.right >= wall.lower.left and \
        ball.rect.left <= wall.lower.right:
        return ball.rect.bottom >= wall.lower.top or \
            ball.rect.top <= wall.upper.bottom
    else:
        return False

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode([x * const.ZOOM for x in const.SIZE])
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("FreeMono", 16)

    # initialize game before starting
    env = new_game()

    # main loop
    while True:
        # set tick rate to 60 per second
        clock.tick(60)

        # close game and terminate process
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        
        # update game state
        pressed_keys = pygame.key.get_pressed()
        env.update(pressed_keys)

        # check for game over
        if env.check_game_over():
            env = new_game()
            continue
        
        # draw screen
        surface = env.draw()
        surface = pygame.transform.scale(surface, [x * const.ZOOM for x in surface.get_size()])
        screen.blit(surface, surface.get_rect())
        pygame.display.flip()
        
        # score is equal to the number of ticks since the start
        env.ball.score += 1

