# from numpy import exp, random, log, append, ones

# class NeuralNetwork():
#     def __init__(self):
#         print('init');

#     def sigmoid(self, x):
#         """
#         Sigmoid function, maps value between 0 and 1

#         :param x: Value to be converted
#         :returns: Probability of value
#         """

#         return 1.0 / (1.0 + exp(-x))

#     def sigmoid_deriv(self, x):
#         """
#         Derivative of sigmoid function, used to determine confidence

#         :param x: Weight
#         :returns: Confidence of weight
#         """

#         return self.sigmoid(x) * (1 - self.sigmoid(x))

#     def set_weights(self, seed = 1):

#         # Empty or initialize weights
#         self.weights = []

#         # Seed random generator
#         random.seed(seed)

#         # Determine network layer sizes
#         input_layer_size = self.train_data.shape[1]
#         output_size = self.train_target.shape[1]
#         layer_sizes = [input_layer_size] + self.hidden_layer_sizes + [output_size]

#         for layer_index, size in enumerate(layer_sizes):
#             if layer_index > 0:
#                 layer = 2 * random.rand(size, layer_sizes[l - 1] + 1) - 0.5
#                 self.weights[layer_index] = layer

#     def cost(self, target, prediction):
#         """ Determine how well network did """
#         log_fix = .000001

#         return (-1.0 / len(target)) * (target * log(prediction + log_fix) + ((1 - target) * log(1 - prediction + log_fix))).sum()

#     def predict(self, inputs):
        
#         predict_layers = [inputs]

#         for layer_index, weight in enumerate(self.weights):
#             if inputs[layer_index].ndim == 1:
#                 inputs[layer_index].resize(1, inputs[layer_index].shape[0])
#             layer = predict_layers[layer_index].dot(weight.T)
#             predict_layers.append(self.sigmoid(layer))

#         return predict_layers, predict_layers[len(self.weights)]

#     def back_propagate(self, layers, outputs):

#         prediction = layers[len(self.weights)]

#         delta_list = []

#         delta = prediction - outputs
#         if (delta.ndim == 1)
#             delta.resize(1, len(delta))
#         delta_list.append(delta)

#         for index in range(len(self.weights) - 1, 0, -1):
#             delta = delta.dot(self.weights[index][:,1:]) * (layers[index][:,1:] * (1 - layers[index][:,1:]))
#             delta_list.append(delta)

#         delta_list.reverse()

#         gradient_list = []
#         for index in range(len(self.weights)):
#                 gradient_list.append(delta_list[index].T.dot(layers[index]))




#         def back_prop(self, a_N_backprop, Y_train):
#     """
#     a_N - list of layer outputs with dimensions n_observations by n_units
#     Y_train is n_observations, n_classes
    
#     Returns
#       Theta_Gradient_L
#     """
#     T = len(self.Theta_L)
#     Y_pred = a_N_backprop[T]
#     n_observations = len(Y_pred)

#     # Backprop Error; One list element for each layer
#     delta_N = []

#     # Get Error for Output Layer
#     delta = Y_pred - Y_train
#     if delta.ndim == 1:
#       delta.resize(1, len(delta))
#     delta_N.append( delta )

#     # Get Error for Hidden Layers working backwards (stop before layer 0; no error in input layer)
#     for t in range(T-1,0,-1):
#       delta = delta.dot(self.Theta_L[t][:,1:]) * ( a_N_backprop[t][:,1:] * (1 - a_N_backprop[t][:,1:]) )
#       delta_N.append( delta )
#     # Reverse the list so that delta_N[t] is delta that Theta[t] causes on a_N[t+1]
#     delta_N.reverse()

#     # Calculate Gradient from delta and activation
#     # t is the Theta from layer t to layer t+1
#     Theta_Gradient_L = []
#     for t in range(T):
#       Theta_Gradient_L.append( delta_N[t].T.dot(a_N_backprop[t]) )
      
#     # Create modified copy of the Theta_L for Regularization
#     # Coefficient for theta values from bias unit set to 0 so that bias unit is not regularized
#     regTheta = [np.zeros_like(theta) for theta in self.Theta_L]
#     for t, theta in enumerate(self.Theta_L):
#       regTheta[t][:,1:] = theta[:,1:]

#     # Average Error + regularization penalty  
#     for t in range(T):
#       Theta_Gradient_L[t] = Theta_Gradient_L[t] * (1.0/n_observations) + (self.lmda * regTheta[t])
  
#     return Theta_Gradient_L

import numpy as np
from sklearn.datasets import load_iris, load_digits

class py_nn():
  """
  nn.fit(X, Y, epochs) where X is training data np.array of features, Y is training data of np.array of output classes , epochs is integer specifying the number of training iterations
  For multi-class prediction, each observation in Y should be implemented as a vector with length = number of classes where each position represents a class with 1 for the True class and 0 for all other classes
  For multi-class prediction, Y will have shape n_observations by n_classes

  nn.nn_predict(X) returns vector of probability of class being true or false
  For multi-class prediction, returns a vector for each observation will return a vector where each position in the vector is the probability of a class
  """

  def __init__(self):

    self.Theta_L = []           # List of Theta numpy.arrays
    self.lmda = 1e-5            # Regularization term
    self.hidden_layer_length_list = []
    self.reset_theta()          # Sets self.hidden_layer_length_list to [2]
    self.epochs = 2
    self.learning_rate = 0.5
    self.learning_acceleration = 1.05
    self.learning_backup = 0.5
    self.momentum_rate = 0.1
    
  def reset_theta(self):
    """self.reset_theta sets theta as a single hidden layer with 2 hidden units"""
    self.hidden_layer_length_list = [2]

  def sigmoid(self, z):
    """sigmoid is a basic sigmoid function returning values from 0-1"""
    return 1.0 / ( 1.0 + np.exp(-z) )

  def sigmoidGradient(self, z):
    # Not used
    return self.sigmoid(z) * ( 1 - self.sigmoid(z) )
  
  def initialize_theta(self, input_unit_count, output_class_count, hidden_unit_length_list):
    """
      initialize_theta creates architecture of neural network
      Defines self.Theta_L
      
      Parameters:
        hidden_unit_length_list - List of hidden layer units
        input_unit_count - integer, number of input units (features)
        output_class_count - integer, number of output classes
    """
    self.Theta_L = []
    if not hidden_unit_length_list:
      hidden_unit_length_list = self.hidden_layer_length_list
    else:
      self.hidden_layer_length_list = hidden_unit_length_list

    unit_count_list = [input_unit_count]
    unit_count_list.extend(hidden_unit_length_list)
    unit_count_list.append(output_class_count)
    for layer_index, size in enumerate(unit_count_list):
      if layer_index > 0:
        layer = 2 * np.random.rand(size, unit_count_list[layer_index - 1] + 1) - .5
        self.Theta_L.append(layer / 1000)
    # self.Theta_L = [ 2 * (np.random.rand( unit_count, unit_count_list[l-1]+1 ) - 0.5) for l, unit_count in enumerate(unit_count_list) if l > 0]

  def print_theta(self):
    """print_theta(self) prints self.Theta_L and architecture info to std out"""

    T = len(self.Theta_L)

    print()
    print('NN ARCHITECTURE')
    print('%s Layers (%s Hidden)' % ((T + 1), (T-1)))
    print('%s Thetas' % T)
    print('%s Input Features' % (self.Theta_L[0].shape[1]-1))
    print('%s Output Classes' % self.Theta_L[T-1].shape[0])
    print()
    
    print('Units per layer')
    for t, theta in enumerate(self.Theta_L):
      if t == 0:
        print(' - Input: %s Units' % (theta.shape[1] - 1))
      if t < T-1:
        print(' - Hidden %s: %s Units' % ((t+1), theta.shape[0]))
      else:
        print(' - Output: %s Units' % theta.shape[0])
    print()
    
    print('Theta Shapes')
    for l, theta in enumerate(self.Theta_L):
      print('Theta %s: %s' % (l, theta.shape))
    print()
    
    print('Theta Values')
    for l, theta in enumerate(self.Theta_L):
      print('Theta %s:' % l)
      print(theta)
    print()

  def nn_cost(self, Y, Y_pred):
    """
    nn_cost implements cost function
    
    y is n_observations by n_classes (n_classes = 1 for n_classes <=2)
    pred_y is predicted y values and must be same shape as y
    
    Returns J - list of cost values
    """
    if Y.shape != Y_pred.shape:
      if Y.shape[0] != Y_pred.shape:
        raise ValueError('Wrong number of predictions')
      else:
        raise ValueError('Wrong number of prediction classes')
    
    n_observations = len(Y)
    tiny = 1e-6
    # Cost Function
    a = -1.0 / n_observations
    b = Y * np.log(Y_pred + tiny)
    c = 1 - Y
    d = np.log(1 - Y_pred + tiny)
    return a * (b + (c * d)).sum()
    J = (-1.0/n_observations)*(Y * np.log(Y_pred + tiny) + ((1-Y) * np.log(1-Y_pred + tiny))).sum()

    return J  
  

  def nn_predict(self, X):
    """
    nn_predict calculates activations for all layers, returns prediction for Y

    Parameters
      X is array of input features dimensions n_observations by n_features

    Returns
      a_N is outputs of all units
      a_N[L] is array of predicted Y values dimensions n_observations by n_classes
    """

    m = len(X)
    T = len(self.Theta_L)
    
    a_N_predict = [X]        # List of activations including bias unit for non-output layers

    # Loop through each Theta_List theta
    # t is Theta for calculating layer t+1 from layer t
    for t, theta in enumerate(self.Theta_L):
      # Add bias unit
      if a_N_predict[t].ndim == 1:
        a_N_predict[t].resize(1, a_N_predict[t].shape[0])
      a_N_predict[t] = np.append(np.ones((a_N_predict[t].shape[0],1)), a_N_predict[t], 1)
      
      # Calculate and Append new z and a arrays to z_N and a_N lists
      z = a_N_predict[t].dot(theta.T)
      a_N_predict.append( self.sigmoid(z) )

    return a_N_predict, a_N_predict[T]


  def back_prop(self, a_N_backprop, Y_train):
    """
    a_N - list of layer outputs with dimensions n_observations by n_units
    Y_train is n_observations, n_classes
    
    Returns
      Theta_Gradient_L
    """
    T = len(self.Theta_L)
    Y_pred = a_N_backprop[T]
    n_observations = len(Y_pred)

    # Backprop Error; One list element for each layer
    delta_N = []

    # Get Error for Output Layer
    delta = Y_pred - Y_train
    if delta.ndim == 1:
      delta.resize(1, len(delta))
    delta_N.append( delta )

    # Get Error for Hidden Layers working backwards (stop before layer 0; no error in input layer)
    for t in range(T-1,0,-1):
      delta = delta.dot(self.Theta_L[t][:,1:]) * ( a_N_backprop[t][:,1:] * (1 - a_N_backprop[t][:,1:]) )
      delta_N.append( delta )
    # Reverse the list so that delta_N[t] is delta that Theta[t] causes on a_N[t+1]
    delta_N.reverse()

    # Calculate Gradient from delta and activation
    # t is the Theta from layer t to layer t+1
    Theta_Gradient_L = []
    for t in range(T):
      Theta_Gradient_L.append( delta_N[t].T.dot(a_N_backprop[t]) )
      

    # Average Error + regularization penalty  
    for t in range(T):
      Theta_Gradient_L[t] = Theta_Gradient_L[t] * (1.0/n_observations)
  
    return Theta_Gradient_L

  def fit(self, X_train, Y_train, X_test=None, Y_test=None):
    """
    fit() calls the predict and back_prop functions for the 
    given number of cycles, tracks error and error improvement rates
    
    Parameters:
      X_train - np.array of training data with dimension n_observations by n_features
      Y_train - np.array of training classes with dimension n_observations by n_classes
      epochs -  integer of number of times to update Theta_L
      learning_rate
      momentum_rate
      learning_acceleration
      learning_backup
      X_test - np.array of training data with dimension n_observations by n_features
      Y_test - np.array of training classes with dimension n_observations by n_classes
    Returns
      J_list - list of result of cost function for each epoch
      Learning_rates - list of learning rates used for each epoch
    Notes
      Training and Test data are assumed to be in random order; mini-batch processing does not need to re-randomize
    """
  
    # If no Theta provided, use a 3 layer architecture with hidden_layer units = 2 or y classes or x features
    if not self.Theta_L:
      hidden_units = max(2, len(Y_train[0]), len(X_train[0]))
      self.initialize_theta(len(X_train[0]), len(Y_train[0]), [hidden_units])

    # Initial Learning Rate
    learning_rates = []
    learning_rates.append( self.learning_rate )

    # Initial Weight Change Terms
    weight_change_L = []
    for theta in self.Theta_L:
      weight_change_L.append(np.zeros_like(theta))
  
    # List of results of cost functions
    J_list = [0] * self.epochs
    J_test_list = [0] * self.epochs

    # Initial Forward Pass
    a_N_train, Y_pred = self.nn_predict(X_train)
    # Initial Cost
    J_list[0] = self.nn_cost(Y_train, Y_pred)

    # Test Error
    if Y_test is not None:
      a_N_test, Y_pred_test = self.nn_predict(X_test)
      J_test_list[0] = self.nn_cost(Y_test, Y_pred_test)

    for i in range(1,self.epochs):

      # Back Prop to get Theta Gradients
      Theta_grad = self.back_prop(a_N_train, Y_train)

      # Update Theta with Momentum
      for l, theta_g in enumerate(Theta_grad):
        a = self.learning_rate * theta_g
        b = weight_change_L[l] * self.momentum_rate
        weight_change_L[l] = a + b
        # weight_change_L[l] = self.learning_rate * theta_g + (weight_change_L[l] * self.momentum_rate)
        self.Theta_L[l] = self.Theta_L[l] - weight_change_L[l]

      # Update Units
      a_N_train, Y_pred_new = self.nn_predict(X_train)

      # Check to see if Cost decreased
      J_new = self.nn_cost(Y_train, Y_pred_new)

      if J_new > J_list[i-1]:
        print('x')
        # Reduce learning rate
        self.learning_rate *= self.learning_backup
        # Reverse part of adjustment (add back new learning_rate * Theta_grad); Leave momentum in place
        self.Theta_L = [t + (self.learning_rate * tg) for t, tg in zip(self.Theta_L, Theta_grad)]
        # Cut prior weight_change as an approximate fix to momentum
        weight_change_L = [m * self.learning_backup for m in weight_change_L]

        a_N_train, Y_pred_new = self.nn_predict(X_train)
        J_new = self.nn_cost(Y_train, Y_pred_new)
      else:
        self.learning_rate = np.min((10,self.learning_rate * self.learning_acceleration))

      learning_rates.append(self.learning_rate)    
      J_list[i] = J_new

      if Y_test is not None:
        a_N_test, Y_pred_test = self.nn_predict(X_test)
        J_test_list[i] = self.nn_cost(Y_test, Y_pred_test)

      if i % 100 == 0:
        print('learning rate ', self.learning_rate)

    for t, theta in enumerate(self.Theta_L):
      print('Theta: %s' % t)
      print(np.round(theta, 2))

    print('i:',i,'  - J:',J_list[i])
    print('i:',i,'  - J test:',J_test_list[i])
    
    return J_list, learning_rates, J_test_list


  def translate_to_binary_array(self, target):
    n_obs = len(target)
    unique_targets = np.unique(target)
    n_unique_targets = len(np.unique(target))

    # Translation of target values to array indicies
    target_translation = dict(list(zip(unique_targets, list(range(n_unique_targets)))))

    # Create initial target array with all zeros
    target_array = np.zeros((n_obs, n_unique_targets))
  
    # Set 1 value
    for i, val in enumerate(target):
      target_array[i][target_translation[val]] = 1    

    return target_array


  def train_test_split(self, data_array, target_array, split=.8):
    """
    Split into randomly shuffled train and test sets
    Split on Number of records or Percent of records in the training set
    if split is <= 1 then split is a percent, else split is the number of records
    """

    n_obs = len(data_array)
  
    if split <= 1:
      train_len = int(split * n_obs)
    else:
      train_len = int(np.round(split))

    shuffled_index = list(range(n_obs))
    np.random.shuffle(shuffled_index)

    train_data = data_array[shuffled_index[:train_len]]
    test_data = data_array[shuffled_index[train_len:]]

    train_target = target_array[shuffled_index[:train_len]]
    test_target = target_array[shuffled_index[train_len:]]
  
    print()
    print('Data Set: %d Observations, %d Features' % (data_array.shape[0], data_array.shape[1]))
    print('Training Set: %d Observations, %d Features' % (train_data.shape[0], train_data.shape[1]))
    print('Test Set: %d Observations, %d Features' % (test_data.shape[0], test_data.shape[1]))
    print()
    print('Target Set: %d Observations, %d Classes' % (target_array.shape[0], target_array.shape[1]))
    print('Training Set: %d Observations, %d Features' % (train_target.shape[0], train_target.shape[1]))
    print('Test Set: %d Observations, %d Features' % (test_target.shape[0], test_target.shape[1]))
    print()
  
    return train_data, test_data, train_target, test_target


  def nn_test(self, data_train, target_train, hidden_unit_length_list, epochs, learning_rate, momentum_rate, learning_acceleration, learning_backup, data_test=None, target_test=None):
  
    self.epochs = epochs
    self.learning_rate = learning_rate
    self.momentum_rate = momentum_rate
    self.learning_acceleration = learning_acceleration
    self.learning_backup = learning_backup

    # Initialize Theta based on selected architecture
    self.initialize_theta(data_train.shape[1], target_train.shape[1], hidden_unit_length_list)
  
    # Fit
    J_list, learning_rates, J_test_list = self.fit(data_train, target_train, X_test=data_test, Y_test=target_test)

    # Predict
    a_N, Y_pred = self.nn_predict(data_test)
    print('Given X:')
    print(data_test[:5])
    print('Actual Y, Predicted Y:')
    for p in zip(target_test[:10], np.round(Y_pred[:10],3)):
      print(p)
    print()
    print('CE on Test Set')
    print(self.nn_cost(target_test , Y_pred))

    return target_test, Y_pred, J_list, J_test_list, learning_rates
  

  def iris_test(self, hidden_unit_length_list = [], epochs=2500, learning_rate=0.5, momentum_rate=0.1, learning_acceleration=1.05, learning_backup=0.5):
    data_set = load_iris()

    data = data_set.data
    target = self.translate_to_binary_array(data_set.target)
  
    # Split into train, test sets
    data_train, data_test, target_train, target_test = self.train_test_split(data, target, .75)
  
    return self.nn_test(data_train, target_train, hidden_unit_length_list, epochs, learning_rate, momentum_rate, learning_acceleration, learning_backup, data_test, target_test)

  def digits_test(self, hidden_unit_length_list = [], epochs=10000, learning_rate=1, momentum_rate=0.1, learning_acceleration=1.05, learning_backup=0.5):
    data_set = load_digits()

    data = data_set.data
    target = self.translate_to_binary_array(data_set.target)
  
    # Split into train, test sets
    data_train, data_test, target_train, target_test = self.train_test_split(data, target, .75)
  
    return self.nn_test(data_train, target_train, hidden_unit_length_list, epochs, learning_rate, momentum_rate, learning_acceleration, learning_backup, data_test, target_test)


  def XOR_test(self, hidden_unit_length_list = [], epochs=2500, learning_rate=0.5, momentum_rate=0.1, learning_acceleration=1.05, learning_backup=0.5):
    """
    XOR_test is a simple test of the nn printing the predicted value to std out
    Trains on a sample XOR data set
    Predicts a single value
    Accepts an option parameter to set architecture of hidden layers
    """
  
    # Set Data for XOR Test  
    data_train = np.zeros((4,2))
    data_train[0,0] = 1.
    data_train[1,1] = 1.
    data_train[2,:] = 1.
    data_train[3,:] = 0.

    target_train = np.array([1.,1.,0.,0.]).reshape(4,1)     # Single Class

    # Test X and Y
    data_test = np.array([[1,0],[0,1],[1,1],[0,0]])
    target_test = np.array([[1],[1],[0],[0]])

    print('Training Data: X & Y')
    print(data_train)
    print(target_train)

    return self.nn_test(data_train, target_train, hidden_unit_length_list, epochs, learning_rate, momentum_rate, learning_acceleration, learning_backup, data_test, target_test)

from DataHandler import DataHandler
dh = DataHandler()
nn = py_nn()
# target = nn.translate_to_binary_array(dh.get_target()[:,0][:,0])
target = dh.get_target()[:,0]
data_train, data_test, target_train, target_test = nn.train_test_split(dh.get_data(), target, .8)
nn.nn_test(data_train, target_train, [50], 2500, 0.5, 0.1, 1.05, 0.5, data_test, target_test)