from numpy import exp, array, random, dot, abs, mean
import pickle

class NeuralNetworkTwo:
    def __init__(self, hidden_layers=[100, 10]):
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
        layers = [len(self.train_data[0])] + self.hidden_layers + [1]

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

    def predict(self, inputs, return_layers=False, round_vals=False):
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
        elif round_vals:
            return [self.custom_round(x) for x in curr_layer.reshape(-1)]
        else:
            return curr_layer

    def train(
        self,
        data=None,
        target=None,
        iterations=10000,
        max_error=0,
        log=False
    ):
        """
        Trains the network by adjusting weights of connections to
         move towards more correct predictions

        :param data: List of data
        :param target: List of outputs
        :param iterations: Number of times loop should run
        :param max_error: Learning will stop if error is below this number
        :param log: If should log error amounts
        """

        # Default to set values if not sent in
        if data is None:
            data = self.train_data
        else:
            self.train_data = data

        if target is None:
            target = self.train_target
        else:
            self.train_target = target

        # Check data is consistent and not empty
        assert len(data) == len(target) > 0

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

    def set_data(self, data, target, test_amount=7):
        """
        Sets data and splits it into train and test groups

        :param data: Inputs
        :param target: Outputs
        :param test_amount: Number to test
        """

        self.train_data = data[:-test_amount]
        self.train_target = target[:-test_amount]
        self.test_data = data[-test_amount:]
        self.test_target = target[-test_amount:]

    def test(self, data=None, target=None):
        """
        Test accuracy of neural network on other data

        :param data: Inputs
        :param target: Outputs
        :returns: Accuracy ratio
        """

        # Default to set values if not sent in
        if data is None:
            data = self.test_data

        if target is None:
            target = self.test_target

        # Die if data is inconsistent or empty arrays
        assert len(data) == len(target) > 0

        # Get differences between expected and predicted
        print('')
        print('Target     :', target.reshape(-1))
        actual = self.predict(data, round_vals=True)
        print('Actual     :', actual)
        err_array = list(target.reshape(-1) - actual)
        print('Error Array:', err_array)
        # Return accuracy
        return round(err_array.count(0) / len(err_array), 4)

    def custom_round(self, value):
        """
        Rounds number

        :param value: Value to round
        :returns: Rounded value
        """

        return round(value * 2) / 2