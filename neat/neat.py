import random
import numpy as np

import neat.evolver as evolver
from neat.genome import Genome

POP_SIZE = 100
SURVIVE_RATE = 0.2
MUTATE_RATE = 0.4
BREED_RATE = 0.4
DIVERGE_RATE = 0.2

class Population:
    def get_diverge_threshold(self, n):
        return np.log10(n + 1)

    def __init__(self, num_input, num_output, pop_size=POP_SIZE):
        self.generation = 1
        self.num_input = num_input
        self.num_output = num_output

        self.pop_size = pop_size
        self.num_survive = int(self.pop_size * SURVIVE_RATE)
        self.num_mutate = int(self.pop_size * MUTATE_RATE)
        self.num_breed = self.pop_size - int(self.num_survive + self.num_mutate)
        self.num_diverge = int(self.pop_size * DIVERGE_RATE)

        # creation of initial gene pool
        self.genomes = [
            Genome(self.num_input, self.num_output) for _ in range(self.pop_size)
        ]

        return

    def predicts(self, X):
        Y = [genome.predict(x) for genome, x in zip(self.genomes, X)]
        return Y

    def score_genomes(self, scores):
        for genome, score in zip(self.genomes, scores):
            genome.score = score
        # compute fitness scores that try to give more weight to later improvements
        # not sure if this is optimal
        scores = np.power(scores, np.log(self.generation + 1))
        # scores = np.power(scores, 2)
        total_score = scores.sum()
        fitnesses = scores / total_score
        for genome, fitness in zip(self.genomes, fitnesses):
            genome.fitness = fitness

        return

    def evolve_population(self):
        # sort genomes by its score
        self.genomes.sort(key=lambda genome: genome.fitness, reverse=True)

        # logging
        print("generation: {}".format(self.generation))
        print("best score: {}".format(self.genomes[0].score))
        print("best fitness: {:.4f}".format(self.genomes[0].fitness))
        print("best type: {}".format(self.genomes[0].genome_type))
        print("best shape: {}, {}, {}".format(
            self.genomes[0].x_dim,
            self.genomes[0].h_dim,
            self.genomes[0].y_dim
        ))
        print("----------------")

        survived = evolver.get_survived(self.genomes, self.num_survive)
        threshold = self.get_diverge_threshold(self.generation)
        temp = [(genome.h_dim < threshold) for genome in self.genomes]
        if all(temp):
            mutated = evolver.get_mutated(self.genomes, self.num_mutate - self.num_diverge)
            diverged = evolver.get_diverged(self.genomes, self.num_diverge)
        else:
            mutated = evolver.get_mutated(self.genomes, self.num_mutate)
            diverged = []
        bred = evolver.get_bred(self.genomes, self.num_breed)

        self.genomes = survived + mutated + bred + diverged

        # this is done for purely cosmetic purpose when rendering
        random.shuffle(self.genomes)

        self.generation += 1
        return
