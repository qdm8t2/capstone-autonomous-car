from data_handler import DataHandler
from neural_network import NeuralNetwork

loop_times = 1
accum = 0

dh = DataHandler()

for i in range(0, loop_times):
	nn = NeuralNetwork()
	dh.shuffle()

	nn.set_data(dh.get_data(), dh.get_target())
	nn.fit()
	# nn.save()

	amt =  nn.test()
	accum += amt
	print('Accuracy Ratio:', amt)

print('Average:', accum / loop_times)

# nn.load()
print(nn.predict([dh.convert_image(dh.get_image('test.png'))]))