import sys
import pygame

SIZE = WIDTH, HEIGHT = 640, 480
GRAVITY = 0.5
WHITE = 255, 255, 255

ball = pygame.image.load("blue_ball.png")
ball = pygame.transform.scale(ball, [x * 2 for x in ball.get_size()])

def reset_game():
    global ballrect
    global velocity
    velocity = 0
    ballrect = ball.get_rect()
    ballrect = ballrect.move([160, 160])

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    clock = pygame.time.Clock()

    # initialize game before starting
    reset_game()

    # main loop
    while True:
        # set tick rate to 60 per second
        clock.tick(60)

        # close game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        
        ballrect = ballrect.move((0, velocity))
        velocity = velocity + GRAVITY

        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_SPACE]:
            velocity = -10

        # check if the pc is out of bounds
        if ballrect.top < 0 or ballrect.bottom > HEIGHT:
            reset_game()
        
        # draw screen
        screen.fill(WHITE)
        screen.blit(ball, ballrect)
        pygame.display.flip()

