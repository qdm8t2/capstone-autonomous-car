# import io
# import time
# import threading
# import picamera
# from PIL import Image

# done = False
# lock = threading.Lock()
# pool = []

# iter = 0

# class ImageProcessor(threading.Thread):
# 	def __init__(self):
# 		super(ImageProcessor, self).__init__()
# 		self.stream = io.BytesIO()
# 		self.event = threading.Event()
# 		self.terminated = False
# 		self.start()

	
# 	def run(self):
# 		global done
# 		iter = 0
# 		while not self.terminated:
# 			if self.event.wait(1000):
# 				try:
# 					self.stream.seek(0)
# 					im = Image.open(self.stream)
# 					# Image.save("data/forward/zzz"+ time.strftime("%y%m%d_%H-%M-%S") + ".jpg", format="JPEG")
# 					iter += 1
# 					print(iter)
# 					if iter == 100:
# 						done = True
# 				finally:
# 					self.stream.seek(0)
# 					self.stream.truncate()
# 					self.event.clear()
# 					with lock:
# 						pool.append(self)

# def streams():
# 	while not done:
# 		with lock:
# 			if pool:
# 				processor = pool.pop()
# 			else:
# 				processor = None
# 		if processor:
# 			yield processor.stream
# 			processor.event.set()
# 		else:
# 			time.sleep(0.1)

# with picamera.PiCamera() as camera:
# 	pool = [ImageProcessor() for i in range(4)]
# 	camera.resolution = (640, 480)
# 	camera.framerate = 30
# 	#camera.start_preview()
# 	time.sleep(2)
# 	camera.capture_sequence(streams(), use_video_port=True)

# while pool:
# 	with lock:
# 		processor = pool.pop()
# 	processor.terminated = True
# 	processor.join()