import sys
import random
import pygame

import constants as const

def add_walls(walls):
    if not walls:
        x = const.WIDTH
    else:
        x = walls[-1][0].rect.left + const.WALL_DISTANCE
    
    variance = random.randint(-const.Y_VARIANCE, const.Y_VARIANCE)
    lower_y = (const.HEIGHT // 2) + (const.HOLE_SIZE // 2) \
              + variance
    upper_y = (const.HEIGHT // 2) - (const.HOLE_SIZE // 2) \
              - Wall.image.get_size()[1] + variance
    
    walls.append((Wall(x, lower_y), Wall(x, upper_y)))
    return

def remove_walls(walls):
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
    for i in range(5):
        add_walls(walls)

def load_image(file):
    image = pygame.image.load(file)
    return image

def collision(ball, wall_pair):
    if ball.rect.right >= wall_pair[0].rect.left and \
        ball.rect.left <= wall_pair[0].rect.right:
        return ball.rect.bottom >= wall_pair[0].rect.top or \
            ball.rect.top <= wall_pair[1].rect.bottom
    else:
        return False

class Ball:
    image = load_image("blue_ball.png")

    def __init__(self):
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(const.START_POSITION)
        return

class Wall:
    image = load_image("brick_wall.png")

    def __init__(self, x, y):
        self.rect = self.image.get_rect()
        self.rect = self.rect.move([x, y])
        return

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
        score = score + 1

        # close game and terminate process
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        
        # move the ball
        ball.rect = ball.rect.move((0, velocity))
        velocity = velocity + const.GRAVITY
        
        # move the walls
        for wall_pair in walls:
            for wall in wall_pair:
                wall.rect = wall.rect.move((-const.MOVE_SPEED, 0))
        
        # remove the wall pair if it gets past the screen and add in a new pair
        if walls[0][0].rect.right < 0:
            remove_walls(walls)
            add_walls(walls)

        # jump if the spacebar is pressed
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_SPACE]:
            velocity = const.JUMP_VELOCITY

        # check if the ball is out of bounds
        if ball.rect.top < 0 or ball.rect.bottom > const.HEIGHT:
            reset_game()
            continue
        
        # check if the ball has collided with a wall
        if collision(ball, walls[0]):
            reset_game()
            continue
        
        # draw screen
        canvas.fill(const.WHITE)
        canvas.blit(ball.image, ball.rect)
        for wall_pair in walls:
            for wall in wall_pair:
                canvas.blit(wall.image, wall.rect)
        text = font.render("Score: " + str(score), True, const.BLACK)
        canvas.blit(text, (0, 0))

        zoomed_canvas = pygame.transform.scale(canvas, [x * const.ZOOM for x in canvas.get_size()])
        screen.blit(zoomed_canvas, zoomed_canvas.get_rect())
        pygame.display.flip()

