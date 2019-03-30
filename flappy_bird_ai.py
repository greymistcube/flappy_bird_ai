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
        self.rect = self.rect.move(const.START_POSITION)
        return
    
    def move(self, velocity):
        self.rect = self.rect.move((0, velocity))
        return

class Wall:
    image = load_image("brick_wall.png")

    def __init__(self, x, y):
        self.lower = self.image.get_rect()
        self.upper = self.image.get_rect()
        lower_y = y + (const.HOLE_SIZE // 2)
        upper_y = y - ((const.HOLE_SIZE // 2) + self.image.get_size()[1])
        self.lower = self.lower.move((x, lower_y))
        self.upper = self.upper.move((x, upper_y))
        self.x = x
        self.y = y
        return
    
    def move(self, speed):
        self.lower = self.lower.move((-speed, 0))
        self.upper = self.upper.move((-speed, 0))
        return

def add_wall(walls):
    # if no wall exists, add one at the right end of the screen
    # otherwise, add one some distance away from the right-most one
    if not walls:
        x = const.WIDTH
    else:
        x = walls[-1].x + const.WALL_DISTANCE
    
    variance = random.randint(-const.Y_VARIANCE, const.Y_VARIANCE)
    y = (const.HEIGHT // 2) + variance

    walls.append(Wall(x, y))
    return

def remove_wall(walls):
    walls.pop(0)
    return

def reset_game():
    global ball
    global walls
    global velocity
    global score
    score = 0
    velocity = 0
    ball = Ball()
    walls = []
    for _ in range(5):
        add_wall(walls)

def collision(ball, walls):
    wall = walls[0]
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
    reset_game()

    # main loop
    while True:
        # set tick rate to 60 per second
        clock.tick(60)

        # close game and terminate process
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        
        # move the ball
        ball.move(velocity)
        velocity = velocity + const.GRAVITY
        
        # move the walls
        for wall in walls:
            wall.move(const.MOVE_SPEED)
        
        # remove the wall pair if it gets past the screen and add in a new pair
        if walls[0].lower.right < 0:
            remove_wall(walls)
            add_wall(walls)

        # jump if the spacebar is pressed
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_SPACE]:
            velocity = const.JUMP_VELOCITY

        # check if the ball is out of bounds
        if ball.rect.top < 0 or ball.rect.bottom > const.HEIGHT:
            reset_game()
            continue
        
        # check if the ball has collided with a wall
        if collision(ball, walls):
            reset_game()
            continue
        
        # draw screen
        canvas.fill(const.WHITE)
        canvas.blit(ball.image, ball.rect)
        for wall in walls:
            canvas.blit(wall.image, wall.lower)
            canvas.blit(wall.image, wall.upper)
        text = font.render("Score: " + str(score), True, const.BLACK)
        canvas.blit(text, (0, 0))

        zoomed_canvas = pygame.transform.scale(canvas, [x * const.ZOOM for x in canvas.get_size()])
        screen.blit(zoomed_canvas, zoomed_canvas.get_rect())
        pygame.display.flip()
        
        # score is equal to the number of ticks since the start
        score = score + 1



