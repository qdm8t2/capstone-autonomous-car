import numpy as np
from scipy.misc import imsave, imresize, imread
from time import time
from DataHandler import DataHandler
import pickle

class NeuralNetwork():
    """
    Neural network using backpropagation
    """

    def __init__(self, hidden_layer_sizes=[50], image_processor=None, debug_enabled=False):
        """
        Constructor

        :param hidden_layer_sizes: Array of hidden layer node amounts
        :param image_processor: The processor to send images through
        """

        # Set public variables
        self.hidden_layer_sizes = hidden_layer_sizes
        self.image_processor = image_processor
        self.debug_enabled = debug_enabled

    def _shuffle_data_(self, data, target):
        """
        Shuffles data and target data in same way

        :param data: Input data
        :param target: Output data
        :returns data: Shuffled input data
        :returns target: Shuffled output data
        """

        # Get random permutation
        p = np.random.permutation(len(data))

        # Apply random permutation to data and target
        return np.array(data)[p], np.array(target)[p]

    def _set_data_(self, data, target, test_percent):
        """
        Set the data to be used for training and testing

        :param data: The images
        :param target: The associated action
        :param test_percent: The percent of total data to test
        """

        # Shuffle
        data, target = self._shuffle_data_(data, target)

        # Determine where to split at
        split_at = int((1 - test_percent) * len(data))

        # Split data
        self.data = data[:split_at]
        self.test_data = data[split_at:]

        # Split targets
        self.target = target[:split_at]
        self.test_target = target[split_at:]

        # Initialize weights
        self._initialize_weights_()

    def load_data(self, files=None, test_percent=0.15):
        """
        Loads data into neural net

        :param file: The files to load
        :param test_percent: Percent of images to use as test data
        """

        # Data Handler
        if files != None:
            dh = DataHandler(files, self.debug_enabled)
        else:
            dh = DataHandler(debug_enabled=self.debug_enabled)

        # Get data, target
        data = dh.get_data()
        target = dh.get_target()

        # Process image
        if self.image_processor != None:
            data = [self.image_processor.process(im) for im in data]

        self._set_data_(data, target, test_percent)

    def save(self, filename='data/models/current.pkl'):
        """
        Save network to a location

        :param filename: Where to save to
        """

        # Data object to store
        data = {
            'weights': self.weights,
            'image_processor': self.image_processor
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
        self.image_processor = data['image_processor']

    def _sigmoid_(self, x):
        """
        Sigmoid function to convert numbers to probabilities (between 0 and 1)

        :param x: Value to convert
        :returns: Probability [0,1]
        """
        return 1.0 / ( 1.0 + np.exp(-x) )

    def _initialize_weights_(self):
        """
        Initialize the weights between layers
        """

        # Empty or initialize weights
        self.weights = []

        # Determine first and last layer sizes
        input_layer_size = self.data.shape[1]
        output_size = self.target.shape[1]

        # Get list of layer sizes [input, hidden_layer0, hidden_layer1, ..., hidden_layerN, output]
        layer_sizes = [input_layer_size] + self.hidden_layer_sizes + [output_size]

        # Generate the weights
        self.weights = [ 2 * (np.random.rand(size, layer_sizes[layer_index - 1] + 1) - 0.5) for layer_index, size in enumerate(layer_sizes) if layer_index > 0]

    def _cost_(self, target, prediction):
        """
        Determine success of prediction

        :param target: The expected predictions
        :param prediction: The actual predictions
        :returns: How successful the prediction was
        """

        # To keep from doing log(0) and getting errors
        log_fix = .000001
        
        # Determine accuracy
        a = target * np.log(prediction + log_fix)
        b = (1 - target) * np.log(1 - prediction + log_fix)

        # Average costs and negate
        return (a + b).sum() / len(target) * -1

    def predict(self, inputs, process_image=False):
        """
        Make a prediction

        :param inputs: The data to predict from
        :param process_image: If inputs should be processed
        :returns: Total prediction and final prediction
        """

        # Process images if they haven't been already
        if process_image:
            inputs = np.array([self.image_processor.process(im) for im in inputs])

        # Array of predictions
        predict_layers = [inputs]

        # Loop through each layer
        for layer_index, layer in enumerate(self.weights):

            # Handle bias
            if predict_layers[layer_index].ndim == 1:
                predict_layers[layer_index].resize(1, predict_layers[layer_index].shape[0])
            bias = np.ones((predict_layers[layer_index].shape[0], 1))
            # Add bias row
            predict_layers[layer_index] = np.append(bias, predict_layers[layer_index], 1)

            # Calculate current layer's prediction
            layer = predict_layers[layer_index].dot(layer.T)
            # Add layer to predictions
            predict_layers.append(self._sigmoid_(layer))

        # Return all prediction layers and last
        return predict_layers, predict_layers[len(self.weights)]

    def _get_adjustments_(self, predict_layers):
        """
        Determine adjustment amounts for weights

        :param predict_layers: The predictions for each layer
        :returns: Gradient list to apply to the weights
        """

        # Quick calculations for later
        num_layers = len(self.weights) # Number of layers in nn (basically len(hidden_layer_sizes) + 2)
        prediction = predict_layers[num_layers] # Final prediction
        num_inputs = len(prediction) # Number of inputs

        # List of errors
        error_list = []

        # Get final error
        error = prediction - self.target

        # Print error
        if self.debug_enabled:
            print('error: ', np.average(np.abs(error)))

        # Handle bias
        if error.ndim == 1:
            error.resize(1, len(error))

        # Add error to list
        error_list.append(error)

        # Calculate hidden layer error in reverse
        # Skip input layer
        for i in range(num_layers - 1, 0, -1):
            curr_weights = self.weights[i][:,1:]
            curr_layer = predict_layers[i][:,1:]

            # Determine error for current layer
            error = error.dot(curr_weights) * (curr_layer * (1 - curr_layer))

            # Add to error list
            error_list.append(error)

        # Flip error list so it is back in order
        #  since we added in reverse
        error_list.reverse()

        # Determine gradients for each layer
        gradient_list = []
        for i in range(num_layers):
            gradient = error_list[i].T.dot(predict_layers[i])
            gradient_list.append(gradient)

        # Average the error out
        for i in range(num_layers):
            gradient_list[i] /= num_inputs

        # Return list of gradients
        return gradient_list    

    def train(self, iterations=2500, learning_rate=0.1, learning_accel=1.05, learning_backoff=0.1, momentum=0.1):
        """
        Trains the neural network

        :param iterations: Number of times to run the training loop
        :param learning_rate: Initial learning speed
        :param learning_accel: How quickly it increases learning speed
        :param learning_backoff: How fast it regresses when wrong
        :param momentum: Momentum used to avoid local minima
        :returns: List of costs
        """

        # Initialize change list to zeros
        change_list = []
        for layer in self.weights:
            change_list.append(np.zeros_like(layer))
    
        # List of costs for each iteration
        cost_list = [0] * iterations

        # Make initial prediction
        layers, prediction = self.predict(self.data)

        # Determine initial cost
        cost_list[0] = self._cost_(self.target, prediction)

        # Adjust -> Predict loop
        for i in range(1, iterations):

            # Get gradients for backpropagation
            gradient_list = self._get_adjustments_(layers)

            # Update weights
            for j, gradient in enumerate(gradient_list):
                # Determine change amount
                adjusted_learning_rate = learning_rate * gradient
                adjusted_change = change_list[j] * momentum
                change_list[j] = adjusted_learning_rate + adjusted_change

                # Update weight with change amount
                self.weights[j] = self.weights[j] - change_list[j]

            # Make new prediction
            layers, new_prediction = self.predict(self.data)

            # Determine new cost
            new_cost = self._cost_(self.target, new_prediction)

            # Handle cost increase
            if new_cost > cost_list[i - 1]:

                # Reduce learning rate by backoff percent
                learning_rate *= learning_backoff

                # Add the adjusted learning rate back in to the weights
                j = 0
                for weight, gradient in zip(self.weights, gradient_list):
                    adjusted_learning_rate = learning_rate * gradient
                    self.weights[j] = weight + adjusted_learning_rate
                    j += 1

                # Reduce changes by learning backoff
                change_list = [change * learning_backoff for change in change_list]

                # Make new prediction
                layers, new_prediction = self.predict(self.data)

                # Determine cost again
                new_cost = self._cost_(self.target, new_prediction)

            # Handle cost decrease
            else:
                # Increase learning rate
                learning_rate *= learning_accel

                # Max out learning rate at 10
                if learning_rate > 10:
                    learning_rate = 10

            # Add cost to cost list
            cost_list[i] = new_cost

            # Debug information
            if self.debug_enabled:
                # Print out iteration info
                print('iteration: ', i);
                print('learning rate: ', learning_rate)
                print('cost: ', new_cost)

        # Debug information
        if self.debug_enabled:
            # Print out weights
            for j, layer in enumerate(self.weights):
                print('Layer: %s' % j)
                print(np.round(layer, 2))

            # Print out cost list
            print('i:', i, '  - J:', cost_list[i])
        
        # Return costs
        return cost_list

    def test(self, save_failures=False, failure_directory="data/bad/"):
        """
        Perform test to see accuracy of neural net

        :param save_failures: If incorrectly guessed images should be saved
        :param failure_directory: Where to save bad images
        """

        # Make prediction
        layers, prediction = self.predict(self.test_data)

        # Log input
        print('Input:')
        print(self.test_data[:5])

        # Log prediction and expected output
        print('Expected Output, Predicted Output')
        for guess_pair in zip(self.test_target, np.round(prediction, 3)):
            print(guess_pair)
        print()

        # Log costs
        print('Costs:')
        print(self._cost_(self.test_target, prediction))

        # Loop variables
        num_correct = 0 # Correct predictions
        i = 0 # Iterator

        # Loop through each prediction
        for expected, actual, image in zip(self.test_target, prediction, self.test_data):

            # Determine indexes
            expected_index = np.argmax(expected)
            actual_index = np.argmax(actual)

            # Increase iterator
            i += 1

            # Handle correct guess
            if expected_index == actual_index:
                num_correct += 1
            # Save image if settings is set and incorrect guess
            elif save_failures:

                # Data Handler
                dh = DataHandler()

                # Get expected and actual directions
                expected_dir = dh.index_to_description(expected_index)
                actual_dir = dh.index_to_description(actual_index)

                # Create fil name
                file = failure_directory
                file += str(round(time() * 1000))
                file += "-" + str(i) + "-"
                file += expected_dir + "-not-"
                file += actual_dir + ".png"

                # Save image
                imsave(file, (image.reshape(50, 50) * 255).astype('uint8'))

        # Log accuracy info
        print('Correct: ', (num_correct / len(prediction)))
        print('Number tested: ', len(prediction))

class ImageProcessor():
    def process(self, image):
        return imresize(image, (50, 50)).flatten() / 255

# # Training and save example
# nn = NeuralNetwork(image_processor=ImageProcessor(), debug_enabled=True)
# nn.load_data()
# try:
#     nn.train()
# except:
#     pass
# nn.test()
# # nn.save()

# # Load and predict sample
# dh = DataHandler(initialize_files=False)
# nn = NeuralNetwork()
# nn.load()
# im = imread('data/forward/img_19-35-33-084182.jpg', flatten=True)
# a, prediction = nn.predict([im], True)
# prediction_index = dh.determine_index(prediction)
# print("Prediction:", dh.index_to_description(prediction_index))