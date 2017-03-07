import glob
import numpy
from PIL import Image

class DataHandler:
	def __init__(self, files=glob.glob('data/**/*.png')):
		self.data = []
		self.target = []
		self.handle_files(files)

	def handle_files(self, files):
		for file in files:
			image = self.get_image(file)
			self.data.append(self.convert_image(image))
			self.target.append(self.determine_type(file))
		self.shuffle()

	def get_image(self, file):
		return Image.open(file)

	def convert_image(self, image):
		pic = []
		for pixel in iter(image.getdata()):
			pic.append(self.convert_pixel(pixel))
		return pic

	def convert_pixel(self, pixel):
		return (pixel[0] + pixel[1] + pixel[2]) / 3

	def determine_type(self, file):
		if file.find('left') != -1:
			return 0
		elif file.find('right') != -1:
			return 1
		else:
			return 2

	def shuffle(self):
		assert len(self.data) == len(self.target)
		p = numpy.random.permutation(len(self.data))
		self.data = numpy.array(self.data)[p]
		self.target = numpy.array(self.target)[p]

	def get_data(self):
		return self.data

	def get_target(self):
		return self.target