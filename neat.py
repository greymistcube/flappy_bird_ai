import numpy as np
import random
import copy

class Population:
    pop_size = 100
    top_survival = 20
    mutate = 40
    breed = 40

    def __init__(self):
        self.generation = 1
        return
    
    def evolve(self):
        return

class Genome:
    def __init__(self, num_inputs, num_outputs, random_weights=True):
        self.num_inputs = num_inputs
        self.num_outputs = num_outputs
        # self.num_hiddens = 1
        self.score = 0
        
        self.bias = 10 ** random.randint(0, 4)

        if random_weights:
            self.w1 = (np.random.random((
                1, num_inputs + 1
                )) - 0.5)
            self.w2 = (np.random.random((
                num_outputs, 1
                )) - 0.5)
        else:
            self.w1 = np.zeros((1, num_inputs + 1))
            self.w2 = np.zeros((num_outputs, 1))
        return

    def mutate(self):
        prob = 0.5
        mask_one = np.random.choice(
            [0, 1],
            size = self.w1.shape,
            p=[1 - prob, prob]
        )
        mask_two = np.random.choice(
            [0, 1],
            size = self.w2.shape,
            p=[1 - prob, prob]
        )
        var_one = (np.random.random(self.w1.shape) - 0.5) * 0.1
        var_two = (np.random.random(self.w2.shape) - 0.5) * 0.1

        self.w1 = self.w1 + (var_one * mask_one)
        self.w2 = self.w2 + (var_two * mask_two)
        return
    
    def add_hidden_node(self):
        self.w1 = np.append(
            self.w1,
            (np.random.random((1, self.num_inputs + 1)) - 0.5) * 0.1,
            axis=0
            )
        self.w2 = np.append(
            self.w2,
            (np.random.random((self.num_outputs, 1)) - 0.5) * 0.1,
            axis=1
        )
        # self.num_hiddens = self.num_hiddens + 1
        return 
    
    def predict(self, inputs):
        # append bias to inputs
        inputs = np.append(self.bias, inputs)

        # multiply by weight and push to hidden
        hiddens = np.dot(self.w1, inputs.reshape(-1, 1))

        # apply activation to hidden
        hiddens = 1 / (1 + np.exp(-1 * hiddens))

        # multiply by weight and push to output
        outputs = np.dot(self.w2, hiddens.reshape(-1, 1))

        # apply activation and return result
        outputs = 1 / (1 + np.exp(outputs))
        outputs = np.ndarray.flatten(outputs > 0.5)
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

    prob = 0.5
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
    var1 = (np.random.random(mutated.w1.shape) - 0.5) * 0.1
    var2 = (np.random.random(mutated.w2.shape) - 0.5) * 0.1

    mutated.w1 = mutated.w1 + (var1 * mask1)
    mutated.w2 = mutated.w2 + (var2 * mask2)
    
    return mutated