import sys
import pygame

pygame.init()

size = width, height = 640, 480
velocity = 0
gravity = 0.5
white = 255, 255, 255

screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

ball = pygame.image.load("blue_ball.png")
ball = pygame.transform.scale(ball, [x * 2 for x in ball.get_size()])

def reset_game():
    global ballrect
    global velocity
    velocity = 0
    ballrect = ball.get_rect()
    ballrect = ballrect.move([160, 160])

reset_game()

while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    
    ballrect = ballrect.move((0, velocity))
    velocity = velocity + gravity
    pressed_keys = pygame.key.get_pressed()
    
    if pressed_keys[pygame.K_SPACE]:
        velocity = -10

    if ballrect.top < 0 or ballrect.bottom > height:
        reset_game()
    
    screen.fill(white)
    screen.blit(ball, ballrect)
    pygame.display.flip()

