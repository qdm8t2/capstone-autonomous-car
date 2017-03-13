from DataHandler import DataHandler
# from NeuralNetwork import NeuralNetwork
from NeuralNetworkTwo import NeuralNetworkTwo

dh = DataHandler()
nn = NeuralNetworkTwo()

# nn.load()
nn.train(dh.get_data(), dh.get_target(), max_error=.02, log=True)
# nn.save()
# print(nn.predict([dh.convert_image(dh.get_image('test.png'))]))