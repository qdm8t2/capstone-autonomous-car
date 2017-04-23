import ImageManipulator
import glob
from PIL import Image

processor = ImageManipulator.ImageManipulator()
stopP = ImageManipulator.IMStop()
roadP = ImageManipulator.IMRoad()

images = glob.glob('images/**/*.*')

for item in images:
    try:
        pil_im = Image.open(item)
    except IOError:
        print("\n error opening image: " + item + "\n")
    with pil_im:
        if "stop" not in item:
            print(roadP.process(pil_im))
        elif "stop" in item:
            print(stopP.process(pil_im))


