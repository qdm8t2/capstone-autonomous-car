from numpy import exp, array, random, dot, abs, mean
import pickle

class NeuralNetworkTwo:
    def __init__(self, hidden_layers=[25, 10]):
        """
        Constructor

        :param hidden_layers: Array of hidden layer node amounts
        """
        self.hidden_layers = hidden_layers

    def sigmoid(self, x):
        """
        Sigmoid function, maps value between 0 and 1

        :param x: Value to be converted
        :returns: Probability of value
        """

        return 1 / (1 + exp(-x))

    def sigmoid_deriv(self, x):
        """
        Derivative of sigmoid function, used to determine confidence

        :param x: Weight
        :returns: Confidence of weight
        """

        return x * (1 - x)

    def set_weights(self, seed=1):
        """
        Set's weights for node connections

        :param seed: Seed used in random function
        """
        # Seed the random function
        random.seed(seed)

        # Create list of all layers
        #  input + hidden + output
        layers = [len(self.data[0])] + self.hidden_layers + [1]

        # Initialize weights
        self.weights = []

        # Set random wights
        for i in range(len(layers) - 1):
            weight_layer = self.create_weight_layer(
                layers[i],
                layers[i+1]
            )
            self.weights.append(weight_layer)

    def create_weight_layer(self, num_input, num_output):
        """
        Creates a layer with random weights connection input and output

        :param num_input: The number of input nodes
        :param num_output: The number of output nodes
        :returns: Weighted matrix with weights between -1 and 1, with mean 0 
        """
        return 2 * random.random((num_input, num_output)) - 1

    def predict(self, inputs, return_layers=False):
        """
        Predicts values of inputs

        :param inputs: The inputs to predict
        :param return_layers: If should return individual layers
        :returns: Prediction or layers
        """

        layers = []
        curr_layer = inputs

        # Loop for each layer of weights
        for weight in self.weights:
            # Collect layers if need to return them
            if return_layers:
                layers.append(curr_layer)

            # Apply current layer's weights to previous layer's values
            curr_layer = self.sigmoid(
                dot(curr_layer, weight)
            )

        if return_layers:
            layers.append(curr_layer)
            return layers
        else:
            return curr_layer

    def train(self, data, target, iterations=10000, max_error=0, log=False):
        """
        Trains the network by adjusting weights of connections to
         move towards more correct predictions

        :param data: List of data
        :param target: List of outputs
        :param iterations: Number of times loop should run
        :param max_error: Learning will stop if error is below this number
        :param log: If should log error amounts
        """

        self.data = data

        # Init weights
        self.set_weights()

        # Train
        for i in range(iterations):
            # Pass training data through the neural network
            #  and get layers
            layers = self.predict(data, True)
            layer_len = len(layers)

            adjusts = []

            # Determine final error
            error = target - layers[-1]
            avg_error = mean(abs(error))

            if log and (i % 10) == 0:
                print('Error:', str(avg_error))

            # Quit if error 
            if avg_error < max_error:
                break

            # Determine weight adjustment for first weights
            adjust = error * self.sigmoid_deriv(layers[-1])
            adjusts.append(adjust)

            # Determine weight adjustments for other weights
            for j in range(2, layer_len):
                # Take dot product of next layer's (+1) adjustments
                #  and next layer's weights
                error = adjust.dot(self.weights[-j+1].T)

                # Determine adjustment amount
                adjust = error * self.sigmoid_deriv(layers[-j])
                adjusts.append(adjust)

            # Adjust the weights
            for j in range(len(self.weights)):
                self.weights[j] += layers[j].T.dot(adjusts[-j-1])

        if log:
            print('Final Error:', str(avg_error))

    def save(self, filename='data/models/current.pkl'):
        """
        Save network to a location

        :param filename: Where to save to
        """

        # Data object to store
        data = {
            'weights': self.weights,
        }

        # Write to file
        with open(filename, 'wb') as fid:
            pickle.dump(data, fid)

    def load(self, filename='data/models/current.pkl'):
        """
        Load network from file

        :param filename: File data is stored in
        """

        with open(filename, 'rb') as fid:
            data = pickle.load(fid)

        self.weights = data['weights']