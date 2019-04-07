import random
import numpy as np

import neat.evolver as evolver
from neat.genome import Genome

class Population:
    # for now pop_size should be the sum of the rest
    pop_size = 200
    num_survive = 40
    num_mutate = 80
    num_breed = 80
    num_diverge = 0

    def __init__(self, num_input, num_output):
        self.generation = 1
        self.num_input = num_input
        self.num_output = num_output

        # creation of initial gene pool
        self.genomes = [
            Genome(self.num_input, self.num_output) for _ in range(self.pop_size)
        ]

        return

    def predicts(self, X):
        y = [genome.predict(x) for genome, x in zip(self.genomes, X)]
        return y

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
        print("best fitness: {}".format(self.genomes[0].fitness))
        print("best type: {}".format(self.genomes[0].genome_type))
        print("------------------------")
        print([genome.h_dim for genome in self.genomes[:10]])

        survived = evolver.get_survived(self.genomes, self.num_survive)
        mutated = evolver.get_mutated(self.genomes, self.num_mutate)
        bred = evolver.get_bred(self.genomes, self.num_breed)
        diverged = evolver.get_diverged(self.genomes, self.num_diverge)

        self.genomes = survived + mutated + bred + diverged

        # this is done for purely cosmetic purpose when rendering
        random.shuffle(self.genomes)

        self.generation += 1
        return
