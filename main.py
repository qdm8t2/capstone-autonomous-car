from data_handler import DataHandler
from neural_network import NeuralNetwork

dh = DataHandler()
nn = NeuralNetwork()

nn.set_data(dh.get_data(), dh.get_target())
nn.fit()
nn.save()

print('Accuracy Ratio:', nn.test())

# nn.load()
# print(nn.predict([dh.convert_image(dh.get_image('data/right/14.png'))]))