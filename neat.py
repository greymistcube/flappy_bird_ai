import random
import copy
import numpy as np

class Population:
    pop_size = 200
    num_survive = 20
    num_mutate = 80
    num_breed = 60
    num_add_node = 40
    num_new_blood = 20

    def __init__(self, num_inputs, num_outputs):
        self.generation = 1
        self.genomes = []
        self.num_inputs = num_inputs
        self.num_outputs = num_outputs

        for _ in range(self.pop_size):
            self.genomes.append(Genome(self.num_inputs, self.num_outputs))
        return

    """
    def evolve(self):
        self.genomes.sort(key=lambda x: x.score, reverse=True)
        self.genomes = self.genomes[:self.num_survive]
        print([int(genome.score) for genome in self.genomes])
        print([int(genome.age) for genome in self.genomes])
        print([genome.num_hiddens for genome in self.genomes])
        for genome in self.genomes:
            genome.age += 1
        
        # reset scores for survived genomes
        # for genome in self.genomes:
        #     genome.score = 0
        
        temp = []
        for _ in range(self.num_mutate):
            i = random.randint(0, self.num_survive - 1)
            genome = copy.deepcopy(self.genomes[i])
            # genome.score = 0
            # genome.age = 0
            temp.append(mutate(genome))
        
        for _ in range(self.num_breed):
            temp.append(breed(self.genomes))
        
        for _ in range(self.num_add_node):
            i = random.randint(0, self.num_survive - 1)
            genome = copy.deepcopy(self.genomes[i])
            genome.add_hidden_node()
            # genome.score = 0
            # genome.age = 0
            temp.append(genome)
        
        #for _ in range(self.num_new_blood):
        #    temp.append(Genome(self.num_inputs, self.num_outputs))
        
        self.genomes += temp

        self.generation += 1
        return
    """

    def evolve(self):
        next_gen = []
        scores = np.asarray([genome.score for genome in self.genomes])
        # try to give more weight to later improvements
        # not sure if it is optimal
        scores = np.power(scores, np.log(self.generation + 1))
        total_score = scores.sum()
        fitness = scores / total_score

        next_gen = np.random.choice(
            range(self.pop_size),
            size=self.pop_size - self.num_survive,
            replace=True,
            p=fitness
        ).tolist()

        prev_gen = self.genomes
        self.genomes = []
        for i in next_gen:
            self.genomes.append(mutate(prev_gen[i]))
            self.genomes[-1].score = 0
        prev_gen.sort(key=lambda x: x.score, reverse=True)
        for genome in prev_gen[:self.num_survive]:
            self.genomes.append(copy.deepcopy(genome))
            self.genomes[-1].score = 0

        self.generation += 1
        return

    def predicts(self, all_inputs):
        predicts = []
        for i in range(len(self.genomes)):
            genome = self.genomes[i]
            inputs = all_inputs[i]
            predicts.append(genome.predict(inputs))
        return predicts

    def score_genomes(self, scores):
        for i in range(len(self.genomes)):
            self.genomes[i].score = scores[i]
        return

class Genome:
    mutate_strength = 0.1
    new_node_strength = 0.01
    def __init__(self, num_inputs, num_outputs, random_weights=True):
        self.num_inputs = num_inputs
        self.num_outputs = num_outputs
        self.num_hiddens = 5
        self.score = 0
        self.age = 0
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

    def mutate(self):
        prob = 0.5
        mask_one = np.random.choice(
            [0, 1],
            size=self.w1.shape,
            p=[1 - prob, prob]
        )
        mask_two = np.random.choice(
            [0, 1],
            size=self.w2.shape,
            p=[1 - prob, prob]
        )
        var_one = (np.random.random(self.w1.shape) - 0.5)
        var_two = (np.random.random(self.w2.shape) - 0.5)

        self.w1 = self.w1 + (var_one * mask_one)
        self.w2 = self.w2 + (var_two * mask_two)
        return

    def add_hidden_node(self):
        self.w1 = np.append(
            self.w1,
            (np.random.random((1, self.num_inputs + 1)) - 0.5) * 0.2,
            axis=0
            )
        self.w2 = np.append(
            self.w2,
            (np.random.random((self.num_outputs, 1)) - 0.5) * 0.1,
            axis=1
        )
        self.num_hiddens = self.num_hiddens + 1
        return

    def predict(self, inputs):
        # append bias to inputs
        inputs = np.append(self.bias, inputs)

        # multiply by weight and push to hidden
        hiddens = np.dot(self.w1, inputs.reshape(-1, 1))
        # hiddens = self.layer_output(inputs, self.w1)

        # apply relu activation to hidden
        # sigmoid activation commented out below
        # hiddens = 1 / (1 + np.exp(-1 * hiddens))
        hiddens = hiddens * (hiddens > 0)

        # multiply by weight and push to output
        outputs = np.dot(self.w2, hiddens.reshape(-1, 1))

        # return formatted output
        outputs = np.ndarray.flatten(outputs > 0)
        return np.ndarray.tolist(outputs)

    def set_score(self, score):
        self.score = score
        return

def breed(genomes):
    parents = random.sample(genomes, k=2)
    w1 = breed_weights(parents[0].w1, parents[1].w1)
    w2 = breed_weights(parents[0].w2, parents[1].w2)
    child = Genome(parents[0].num_inputs, parents[0].num_outputs, random_weights=False)
    child.w1 = w1
    child.w2 = w2
    if parents[0].score > parents[1].score:
        child.bias = parents[0].bias
    else:
        child.bias = parents[1].bias
    child.score = 0
    child.age = 0
    child.num_hiddens = max(parents[0].num_hiddens, parents[1].num_hiddens)
    return child

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

def mutate(genome):
    # copy the original and then mutate on it
    mutated = copy.deepcopy(genome)

    prob = 0.1
    mask1 = np.random.choice(
        [0, 1],
        size=mutated.w1.shape,
        p=[1 - prob, prob]
    )
    mask2 = np.random.choice(
        [0, 1],
        size=mutated.w2.shape,
        p=[1 - prob, prob]
    )
    var1 = (np.random.random(mutated.w1.shape) - 0.5)
    var2 = (np.random.random(mutated.w2.shape) - 0.5)

    mutated.w1 = mutated.w1 + (var1 * mask1)
    mutated.w2 = mutated.w2 + (var2 * mask2)

    return mutated
