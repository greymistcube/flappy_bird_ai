import sys
import random
import pygame

import constants as const
import neat

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
        self.alive = True
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
    def __init__(self, num_balls=1, num_walls=5):
        self.balls = []
        self.walls = []
        self.surface = pygame.Surface(const.SIZE)
        for _ in range(num_balls):
            self.add_ball()
        for _ in range(num_walls):
            self.add_wall()
        return
    
    def add_ball(self):
        self.balls.append(Ball())
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
    
    def update(self, jumps):
        # move game objects
        for ball in self.balls:
            ball.move()
            ball.accelerate()
        for wall in self.walls:
            wall.move()

        # remove a wall if it gets past the screen and add in a new one
        if self.walls[0].out_of_bounds():
            self.remove_wall()
            self.add_wall()
        
        # jump
        for i in range(len(jumps)):
            if jumps[i][0]:
                self.balls[i].jump()
        
        # kill balls if necessary
        for ball in self.balls:
            if ball.out_of_bounds() or collision(ball, self.walls):
                ball.alive = False

        # update scores for balls still alive
        for ball in self.balls:
            if ball.alive:
                ball.score += 1
        return
    
    def check_game_over(self):
        # if any ball is alive, it is not game over yet
        # if all balls are dead, it is game over
        for ball in self.balls:
            if ball.alive:
                return False
        return True
    
    def draw(self):
        self.surface.fill(const.WHITE)
        for ball in self.balls:
            if ball.alive:
                self.surface.blit(ball.image, ball.rect)
        for wall in self.walls:
            self.surface.blit(wall.image, wall.lower)
            self.surface.blit(wall.image, wall.upper)
        # text = font.render("Score: " + str(self.ball.score), True, const.BLACK)
        # self.surface.blit(text, (0, 0))
        return self.surface

def new_game(ai):
    if ai == "neat":
        env = GameEnvironment(num_balls=100)
    else:
        env = GameEnvironment()

    return env

def collision(ball, walls):
    wall = walls[0]

    # for the current setup, we only need to check with the first wall
    if ball.rect.right >= wall.lower.left and \
        ball.rect.left <= wall.lower.right:
        return ball.rect.bottom >= wall.lower.top or \
            ball.rect.top <= wall.upper.bottom
    else:
        return False

def get_all_inputs(env):
    all_inputs = []
    for ball in env.balls:
        inputs = []
        inputs.append(ball.y)
        inputs.append(ball.velocity)
        inputs.append(env.walls[0].x)
        inputs.append(env.walls[0].y)
        inputs.append(env.walls[1].x)
        inputs.append(env.walls[1].y)
        all_inputs.append(inputs)
    return all_inputs

def get_all_outputs(population, all_inputs):
    return population.predicts(all_inputs)

if __name__ == "__main__":
    ai = ""
    if len(sys.argv) > 1 and sys.argv[1] == "neat":
        ai = "neat"
        population = neat.Population(num_inputs=6, num_outputs=1)
    
    pygame.init()
    screen = pygame.display.set_mode([x * const.ZOOM for x in const.SIZE])
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("FreeMono", 16)

    # initialize game before starting
    env = new_game(ai)

    # main loop
    while True:
        # set tick rate to 60 per second
        clock.tick(60)

        # close the game and terminate process
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        
        # update game state
        if ai == "neat":
            all_inputs = get_all_inputs(env)
            all_outputs = get_all_outputs(population, all_inputs)
            print(all_outputs)
            env.update(all_outputs)
        else:
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[pygame.K_SPACE]:
                env.update([True])
            else:
                env.update([False])

        # check for game over
        if env.check_game_over():
            env = new_game(ai)
            if ai == "neat":
                population.evolve()
            continue
        
        # draw screen
        surface = env.draw()
        surface = pygame.transform.scale(surface, [x * const.ZOOM for x in surface.get_size()])
        screen.blit(surface, surface.get_rect())
        pygame.display.flip()
        

