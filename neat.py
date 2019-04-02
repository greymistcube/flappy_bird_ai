import numpy as np
import random

class Genome:
    def __init__(self, num_inputs, num_outputs):
        self.num_inputs = num_inputs
        self.num_outputs = num_outputs
        self.num_hiddens = 1
        
        self.bias = 10 ** random.randint(0, 4)

        self.weights_one = (np.random.random((
            1, num_inputs + 1
            )) - 0.5)
        self.weights_two = (np.random.random((
            num_outputs, 1
            )) - 0.5)

        return
    
    def add_hidden_node(self):
        self.weights_one = np.append(
            self.weights_one,
            (np.random.random((1, self.num_inputs + 1)) - 0.5) * 0.1,
            axis=0
            )
        self.weights_two = np.append(
            self.weights_two,
            (np.random.random((self.num_outputs, 1)) - 0.5) * 0.1,
            axis=1
        )
        self.num_hiddens = self.num_hiddens + 1    
    
    def predict(self, inputs):
        # append bias to inputs
        inputs = np.append(self.bias, inputs)

        # multiply by weight and push to hidden
        hiddens = np.dot(self.weights_one, inputs.reshape(-1, 1))

        # apply activation to hidden
        hiddens = 1 / (1 + np.exp(-1 * hiddens))

        # multiply by weight and push to output
        outputs = np.dot(self.weights_two, hiddens.reshape(-1, 1))

        # apply activation and return result
        outputs = 1 / (1 + np.exp(outputs))
        outputs = np.ndarray.flatten(outputs > 0.5)
        return np.ndarray.tolist(outputs)
