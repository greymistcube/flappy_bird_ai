import numpy as np

class Genome:
    def __init__(self, x_dim, y_dim, random_weights=True):
        self.genome_type = "survived"
        self.x_dim = x_dim
        self.y_dim = y_dim
        self.h_dim = 2
        self.score = 0
        self.fitness = 0
        # fixed bias for simplicity
        # for optimal search, inputs should be normalized in advance
        self.bias = 1

        if random_weights:
            self.w1 = np.random.random((
                self.h_dim, self.x_dim + 1
                )) * 2 - 1
            self.w2 = np.random.random((
                self.y_dim, self.h_dim
                )) * 2 - 1
        else:
            self.w1 = np.zeros((self.h_dim, self.x_dim + 1))
            self.w2 = np.zeros((self.y_dim, self.h_dim))
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
        return y
