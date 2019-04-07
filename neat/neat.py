import random
import copy
import numpy as np

# list of constants for convenience
MUTATE_RATE = 0.1
MUTATE_STRENGTH = 0.05
DIVERGE_STRENGTH = 0.1

class Population:
    # for now pop_size should be the sum of the rest
    pop_size = 200
    num_survive = 40
    num_mutate = 80
    num_breed = 80
    num_diverge = 0
    # new_node_rule

    def __init__(self, num_inputs, num_outputs):
        self.generation = 1
        self.num_inputs = num_inputs
        self.num_outputs = num_outputs
        self.evolver = Evolver

        # creation of initial gene pool
        self.genomes = [
            Genome(self.num_inputs, self.num_outputs) for _ in range(self.pop_size)
        ]

        return

    def predicts(self, X):
        y = [genome.predict(x) for genome, x in zip(self.genomes, X)]
        return y

    def score_genomes(self, scores):
        for genome, score in zip(self.genomes, scores):
            genome.score = score
        return

    def evolve(self):
        # sort genomes by its score
        self.genomes.sort(key=lambda genome: genome.score, reverse=True)

        # logging
        print("generation: {}".format(self.generation))
        print("best score: {}".format(self.genomes[0].score))
        print("best type: {}".format(self.genomes[0].genome_type))
        print("------------------------")
        print([genome.num_hiddens for genome in self.genomes[:10]])

        # elite genomes that stays unmodified
        survived = [copy.deepcopy(genome) for genome in self.genomes[:self.num_survive]]

        # compute fitness scores that try to give more weight to later improvements
        # not sure if this is optimal
        scores = np.asarray([genome.score for genome in self.genomes])
        scores = np.power(scores, np.log(self.generation + 1))
        # scores = np.power(scores, 2)
        total_score = scores.sum()
        fitness = scores / total_score

        mutated = np.random.choice(
            self.genomes,
            size=self.num_mutate,
            replace=True,
            p=fitness
        )
        mutated = [self.evolver.mutate(genome) for genome in mutated]

        get_parents = lambda: np.random.choice(
            self.genomes,
            size=2,
            replace=False,
            p=fitness
        )
        bred = [self.evolver.breed(get_parents()) for _ in range(self.num_breed)]

        diverged = np.random.choice(
            self.genomes,
            size=self.num_diverge,
            replace=True,
            p=fitness
        )
        diverged = [self.evolver.add_node(genome) for genome in diverged]

        for genome in survived:
            genome.genome_type = "survived"

        self.genomes = survived + mutated + bred + diverged

        # this is done for purely cosmetic purpose when rendering
        random.shuffle(self.genomes)

        self.generation += 1
        return

class Genome:
    def __init__(self, num_inputs, num_outputs, random_weights=True):
        self.genome_type = "survived"
        self.num_inputs = num_inputs
        self.num_outputs = num_outputs
        self.num_hiddens = 2
        self.score = 0
        self.bias = 1

        if random_weights:
            self.w1 = np.random.random((
                self.num_hiddens, self.num_inputs + 1
                )) * 2 - 1
            self.w2 = np.random.random((
                self.num_outputs, self.num_hiddens
                )) * 2 - 1
        else:
            self.w1 = np.zeros((self.num_hiddens, self.num_inputs + 1))
            self.w2 = np.zeros((self.num_outputs, self.num_hiddens))
        return

    # x, h, and y are input vector, hidden vector, and output vector respectively
    def predict(self, x):
        # append bias to inputs
        x = np.append(self.bias, x)

        # multiply by weight and push to hidden layer
        h = np.dot(self.w1, x.reshape(-1, 1))
        # h = self.layer_output(x, self.w1)

        # apply relu activation to h
        # sigmoid activation commented out below
        # h = 1 / (1 + np.exp(-1 * h))
        h = h * (h > 0)

        # multiply by weight and push to output
        y = np.dot(self.w2, h.reshape(-1, 1))

        # return formatted output
        y = np.ndarray.flatten(y > 0)
        return np.ndarray.tolist(y)

    def set_score(self, score):
        self.score = score
        return

# helper class for evolution of population
class Evolver:
    _mutate_rate = MUTATE_RATE
    _mutate_strength = MUTATE_STRENGTH
    _diverge_strength = DIVERGE_STRENGTH

    # copies a genome and returns a mutated one
    @classmethod
    def mutate(cls, genome):
        mutated = copy.deepcopy(genome)

        prob = cls._mutate_rate / 2
        get_var = lambda shape: np.random.choice(
            [-cls._mutate_strength, 0, cls._mutate_strength],
            size=shape,
            p=[prob, 1 - 2 * prob, prob]
        )
        mutated.w1 = mutated.w1 + get_var(mutated.w1.shape)
        mutated.w2 = mutated.w2 + get_var(mutated.w2.shape)

        mutated.genome_type = "mutated"

        return mutated

    @classmethod
    def breed(cls, parents):
        w1 = breed_weights(parents[0].w1, parents[1].w1)
        w2 = breed_weights(parents[0].w2, parents[1].w2)
        child = Genome(parents[0].num_inputs, parents[0].num_outputs, random_weights=False)
        child.w1 = w1
        child.w2 = w2

        child.num_hiddens = max(parents[0].num_hiddens, parents[1].num_hiddens)

        child.genome_type = "bred"
        return child

    @classmethod
    def add_node(cls, genome):
        diverged = copy.deepcopy(genome)
        diverged.w1 = np.append(
            diverged.w1,
            (np.random.random((1, genome.num_inputs + 1)) - 0.5) * cls._diverge_strength,
            axis=0
            )
        diverged.w2 = np.append(
            diverged.w2,
            (np.random.random((genome.num_outputs, 1)) - 0.5) * cls._diverge_strength,
            axis=1
        )
        diverged.num_hiddens += 1

        diverged.genome_type = "diverged"
        return diverged

# takes two numpy arrays and produces a child by breeding
# either the number of rows or the number of columns of two matrices
# should be the same.
def breed_weights(w1, w2):
    prob = 0.5

    min_shape = min(w1.shape, w2.shape)
    max_shape = max(w1.shape, w2.shape)

    w1_pad = np.zeros(max_shape)
    w2_pad = np.zeros(max_shape)
    w1_pad[:w1.shape[0], :w1.shape[1]] = w1
    w2_pad[:w2.shape[0], :w2.shape[1]] = w2
    w = np.zeros(max_shape)

    mask = np.random.choice([0, 1], size=min_shape, p=(1 - prob, prob))

    min_shape_slice = np.index_exp[:min_shape[0], :min_shape[1]]
    excess_row_slice = np.index_exp[min_shape[0]:, :]
    excess_column_slice = np.index_exp[:, min_shape[1]:]

    w[min_shape_slice] = w1_pad[min_shape_slice] * mask + w2_pad[min_shape_slice] * (1 - mask)
    w[excess_row_slice] = w1_pad[excess_row_slice] + w2_pad[excess_row_slice]
    w[excess_column_slice] = w1_pad[excess_column_slice] + w2_pad[excess_column_slice]

    return np.copy(w)
