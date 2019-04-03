import sys
import random
import pygame

import constants as const

ball = None
walls = []
velocity = 0
score = 0

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

        if self.walls:
             print(self.walls[-1].x)
        self.walls.append(Wall(x, y))
        return
    
    def remove_wall(self):
        self.walls.pop(0)
        return

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
    canvas = pygame.Surface(const.SIZE)
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
        
        # move the ball
        env.ball.move()
        env.ball.accelerate()
        
        # move the walls
        for wall in env.walls:
            wall.move()
        
        # remove a wall if it gets past the screen and add in a new one
        if env.walls[0].out_of_bounds():
            env.remove_wall()
            env.add_wall()

        # jump if the spacebar is pressed
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_SPACE]:
            env.ball.jump()

        # check if the ball is out of bounds
        if env.ball.out_of_bounds():
            env = new_game()
            continue
        
        # check if the ball has collided with a wall
        if collision(env):
            env = new_game()
            continue
        
        # draw screen
        canvas.fill(const.WHITE)
        canvas.blit(env.ball.image, env.ball.rect)
        for wall in env.walls:
            canvas.blit(wall.image, wall.lower)
            canvas.blit(wall.image, wall.upper)
        text = font.render("Score: " + str(env.ball.score), True, const.BLACK)
        canvas.blit(text, (0, 0))

        zoomed_canvas = pygame.transform.scale(canvas, [x * const.ZOOM for x in canvas.get_size()])
        screen.blit(zoomed_canvas, zoomed_canvas.get_rect())
        pygame.display.flip()
        
        # score is equal to the number of ticks since the start
        env.ball.score += 1

