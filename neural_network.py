from sklearn.neural_network import MLPClassifier
import pickle

class NeuralNetwork:
	def __init__(self, clf_file=''):
		if clf_file == '':
			self.clf = MLPClassifier(
				solver='lbfgs',
				alpha=1e-5,
				hidden_layer_sizes=(100, 10),
				random_state=1,
				activation='logistic'
			)
		else:
			self.load(clf_file)

	def set_data(self, data, target, test_amount=7):
		self.train_data = data[:-test_amount]
		self.train_target = target[:-test_amount]
		self.test_data = data[-test_amount:]
		self.test_target = target[-test_amount:]

	def fit(self):
		try:
			self.train_data
			self.train_target
			self.test_data
			self.test_target
		except NameError:
			return False

		self.clf.fit(self.train_data, self.train_target)
		return True

	def predict(self, items):
		return self.clf.predict(items)

	def test(self):
		return self.clf.score(self.test_data, self.test_target)

	def save(self, filename='data/models/current.pkl'):
		with open(filename, 'wb') as fid:
			pickle.dump(self.clf, fid)

	def load(self, filename='data/models/current.pkl'):
		with open(filename, 'rb') as fid:
			self.clf = pickle.load(fid)

