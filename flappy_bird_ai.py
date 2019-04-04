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
        # self.x = const.START_POSITION[0]
        # self.y = random.randint(80, const.HEIGHT - 80)
        self.rect.center = (self.x, self.y)
        self.velocity = 0.0
        self.score = 0
        self.alive = True
        return
    
    def move(self):
        # huge pain by using move instead of center
        self.y = self.y + self.velocity
        self.rect.center = (self.x, self.y)
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
        self.score = 0
        self.num_alive = num_balls
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
            if ball.alive and \
                (ball.out_of_bounds() or collision(ball, self.walls)):
                ball.alive = False
                ball.score = self.score
                self.num_alive -= 1

        self.score += 1
        return
    
    def check_game_over(self):
        return self.num_alive == 0
    
    def draw(self):
        # render game objects
        self.surface.fill(const.WHITE)
        for ball in self.balls:
            if ball.alive:
                self.surface.blit(ball.image, ball.rect)
        for wall in self.walls:
            self.surface.blit(wall.image, wall.lower)
            self.surface.blit(wall.image, wall.upper)

        # render info text
        score_text = font.render(" Score: " + str(self.score), False, const.BLACK)
        alive_text = font.render(" Alive: " + str(self.num_alive), False, const.BLACK)
        self.surface.blit(score_text, (0, 0))
        self.surface.blit(alive_text, (0, 12))
        return self.surface

def new_game(ai):
    if ai == "neat":
        env = GameEnvironment(num_balls=neat.Population.pop_size)
    else:
        env = GameEnvironment()
    return env

def collision(ball, walls):
    # return False
    wall = walls[0]

    # for the current setup, we only need to check with the first wall
    if ball.rect.right >= wall.lower.left and \
        ball.rect.left <= wall.lower.right:
        return ball.rect.bottom >= wall.lower.top or \
            ball.rect.top <= wall.upper.bottom
    else:
        return False

def get_inputs(env):
    inputs = []
    for ball in env.balls:
        # skip dead balls
        if ball.alive:
            # get the next wall
            if env.walls[0].lower.right > ball.rect.left:
                next_wall = env.walls[0]
            else:
                next_wall = env.walls[1]
            # append normalized input
            inputs.append([
                ball.y / const.HEIGHT,
                ball.velocity / 10,
                next_wall.y / const.HEIGHT
            ])
        else:
            inputs.append([0, 0, 0])
    return inputs

def get_outputs(population, inputs):
    return population.predicts(inputs)

def get_scores(env):
    scores = []
    for ball in env.balls:
        scores.append(ball.score)
    return scores

if __name__ == "__main__":
    score_history = []
    ai = ""
    if len(sys.argv) > 1 and sys.argv[1] == "neat":
        ai = "neat"
        population = neat.Population(num_inputs=3, num_outputs=1)
    
    pygame.init()
    screen = pygame.display.set_mode([x * const.ZOOM for x in const.SIZE])
    clock = pygame.time.Clock()
    font = pygame.font.Font("./munro.ttf", 10)

    # initialize game before starting
    env = new_game(ai)

    # main loop
    while True:
        # set tick rate to 60 per second
        if ai == "neat":
            clock.tick(0)
            pass
        else:
            clock.tick(60)

        # close the game and terminate process
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        
        # update game state
        if ai == "neat":
            inputs = get_inputs(env)
            outputs = get_outputs(population, inputs)
            env.update(outputs)
        else:
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[pygame.K_SPACE]:
                env.update([[True]])
            else:
                env.update([[False]])

        # check for game over
        if env.check_game_over():
            if ai == "neat":
                scores = get_scores(env)
                population.score_genomes(scores)
                hiddens = [genome.num_hiddens for genome in population.genomes]
                population.evolve()
                # just some debug info
                print("generation: " + str(population.generation))
                print("final score: " + str(env.score))
            env = new_game(ai)
            continue
        
        # draw screen
        surface = env.draw()
        surface = pygame.transform.scale(surface, [x * const.ZOOM for x in surface.get_size()])
        screen.blit(surface, surface.get_rect())
        pygame.display.flip()
        

