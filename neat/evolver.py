import copy
import numpy as np

from neat.genome import Genome

# list of constants for convenience
MUTATE_RATE = 0.1
DIVERGE_STRENGTH = 0.1
# this is to prevent getting stuck in local minima
mutate_strength_rule = lambda: np.random.choice(
    [0.1, 0.2, 0.4],
    p=[0.9, 0.09, 0.01]
)

def get_survived(genomes, n):
    survived = [
        copy.deepcopy(genome)
        for genome in genomes[:n]
    ]
    for genome in survived:
        genome.genome_type = "survived"
    return survived

def get_mutated(genomes, n):
    p = [genome.fitness for genome in genomes]
    mutated = np.random.choice(
        genomes,
        size=n,
        replace=True,
        p=p
    )
    mutated = [_mutate(genome) for genome in mutated]
    return mutated

def get_bred(genomes, n):
    p = [genome.fitness for genome in genomes]
    # additional layer of logic is required to
    # avoid self breeding
    get_parents = lambda: np.random.choice(
        genomes,
        size=2,
        replace=False,
        p=p
    )
    pairs_of_parents = [get_parents() for _ in range(n)]
    bred = [_breed(parents) for parents in pairs_of_parents]
    return bred

def get_diverged(genomes, n):
    p = [genome.fitness for genome in genomes]
    diverged = np.random.choice(
        genomes,
        size=n,
        replace=True,
        p=p
    )
    diverged = [_diverge(genome) for genome in diverged]
    return diverged

# copies a genome and returns a mutated one
def _mutate(genome):
    mutated = copy.deepcopy(genome)

    prob = MUTATE_RATE / 2
    w_delta = lambda w: np.random.choice(
        [-mutate_strength_rule(), 0, mutate_strength_rule()],
        size=w.shape,
        p=[prob, 1 - (2 * prob), prob]
    )
    mutated.w1 += w_delta(mutated.w1)
    mutated.w2 += w_delta(mutated.w2)

    mutated.genome_type = "mutated"
    return mutated

def _breed(parents):
    # create a new child with topology size at least as big as either parents
    child = Genome(parents[0].x_dim, parents[0].y_dim, random_weights=False)
    child.h_dim = max(parents[0].h_dim, parents[1].h_dim)

    # if both parents have h_dim = 1, then randomly mix weights
    # otherwise, breed them by crossover
    if parents[0].h_dim == 1 and parents[1].h_dim == 1:
        w1 = mix_weights(parents[0].w1, parents[1].w1)
        w2 = mix_weights(parents[0].w2, parents[1].w2)
    else:
        if parents[0].h_dim < parents[1].h_dim:
            small_genome = parents[0]
            large_genome = parents[1]
        else:
            small_genome = parents[1]
            large_genome = parents[0]
        splice_idx = np.random.randint(1, small_genome.h_dim + 1)
        w1 = np.vstack([small_genome.w1[:splice_idx], large_genome.w1[splice_idx:]])
        w2 = np.hstack([small_genome.w2[:, :splice_idx], large_genome.w2[:, splice_idx:]])

    child.w1 = w1
    child.w2 = w2

    child.genome_type = "bred"
    return child

def _diverge(genome):
    diverged = copy.deepcopy(genome)
    diverged.w1 = np.append(
        diverged.w1,
        (np.random.random((1, genome.x_dim + 1)) - 0.5) * DIVERGE_STRENGTH,
        axis=0
        )
    diverged.w2 = np.append(
        diverged.w2,
        (np.random.random((genome.y_dim, 1)) - 0.5) * DIVERGE_STRENGTH,
        axis=1
    )
    diverged.h_dim += 1

    diverged.genome_type = "diverged"
    return diverged

# takes two numpy arrays and produces a child by breeding
# either the number of rows or the number of columns of two matrices
# should be the same.
def mix_weights(w1, w2):
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
