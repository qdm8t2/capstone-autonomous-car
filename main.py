from DataHandler import DataHandler
# from NeuralNetwork import NeuralNetwork
from NeuralNetworkTwo import NeuralNetworkTwo

dh = DataHandler()
nn = NeuralNetworkTwo([50, 10])

# Train til 99% accurate
nn.set_data(dh.get_data(), dh.get_target())
nn.train(max_error=.01, log=True)
nn.save()
print('Accuracy:', nn.test())

# # Train until stopped by user
# nn.set_data(dh.get_data(), dh.get_target())
# try:
# 	nn.train(iterations=5000000, log=True)
# except KeyboardInterrupt:
# 	nn.save()
# print('Accuracy:', nn.test())

# # Load network and test image
# nn.load()
# im = dh.get_image('test.png')
# im = dh.convert_image(im)
# predict = nn.predict([im], round_vals=True)
# description = dh.type_to_description(predict[0])
# print(description)