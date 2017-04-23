from pylab import *
from PIL import Image
from PIL import ImageOps

class ImageManipulator:
    """The ImageManipulation Parent Class"""

    def _Crop(self, pil_im):
        """
        
        :param pil_im: Input Image (opened elsewhere)  
        :return: Output Image
        """
        # after the most recent camera angle change, cropping seems to be not needed


        # Where do we start cropping from?
        halfwidth = pil_im.size[0] / 2  # right now I crop from the center of the image
        halfheight = pil_im.size[
                         1] / 2

        # How much of the image do we want to crop out?
        width = pil_im.size[0] / 2.15  # how much for the width
        height = pil_im.size[1] / 6  # how much for the height


        # apply the crop line one: left edge, two: top edge, three: right edge, four: bottom
        if ((width + halfwidth) > pil_im.size[0]):
            print(" your width is out of bounds, too big, the original width is " + str(
                pil_im.size[0]) + " your proposed size is " + str((width + halfwidth)))
            sys.exit()

        elif ((height + halfheight) > pil_im.size[1]):
            print(" your height is out of bounds, too big, the original height is " + str(
                pil_im.size[1]) + " your proposed size is " + str((height + halfheight)))
            sys.exit()

            # else:                                                                 # actually do the crop
            #    pil_im = pil_im.crop(
            #        (
            #            halfwidth - width,
            #            halfheight - height,
            #            halfwidth + width,
            #            halfheight + halfheight,   #no cropping done on bottom
            #        )
            #    )
        return pil_im                                                   #return the cropped image


    def _Resize(self, pil_im):     #Resizes maintaining aspect ratio, should be done before any of the _Recolor
        """
        
        :param pil_im: Input Image (opened elsewhere)
        :return: Output Image
        """
        size = 100, 100        #defines maximum size
        pil_im.thumbnail(size, Image.ANTIALIAS)  #resizes the image
        return(pil_im)                                  #returns the resized image



class IMRoad(ImageManipulator):
    """
    The Image Manipulation 'road' subclass, handles all images of the track 
    AKA all images not of stop signs 
    
    """
    def __init__(self):
        """
        Constructor 
        """
        ImageManipulator.__init__(self)

    def _Recolor( pil_im):
        """
        Converts to greyscale 
        :return: returns converted image as an ARRAY  
        """

        res = Image.new(pil_im.mode, pil_im.size)                           # converts to greyscale since the convert('L') wasnt working for some reason
        for i in range(0, pil_im.size[0]):
            for j in range(0, pil_im.size[1]):
                pixel = pil_im.getpixel((i, j))  # get a pixel
                red = pixel[0]
                green = pixel[1]
                blue = pixel[2]
                avg = (pixel[0] + pixel[1] + pixel[2]) / 3
                res.putpixel((i, j), (int(avg), int(avg), int(avg)))
        pil_im = res
        pil_im = ImageOps.equalize(pil_im)         #histogram equalization before other tranforms

        pil_im = array(pil_im)                  # convert to array for the transforms

        pil_im = (100.0 / 255) * pil_im + 90  # clamp the values...
        pil_im = 255.0 * (pil_im / 255.0) ** 2  # quadratic transformation

        return pil_im
    def process(self, picture):
        """
        calls other class functions to process the given image
        :param picture: input image (already opened) 
        :return: output image as ARRAY 
        """
        ImageManipulator._Crop(self, picture)
        ImageManipulator._Resize(self, picture)
        return IMRoad._Recolor(picture)



class IMStop(ImageManipulator):
    """The Image Manipulation 'Stopsign' subclass"""
    def __init__(self):
        """
        Constructor
        """
        ImageManipulator.__init__(self)

    def _Recolor(picture):
        """
        Converts image to greyscale leaving red pixels
        :return: converted image as ARRAY
        """
        red_lower_threshold = 90
        green_blue_diff_threshold = 75
        res = Image.new(picture.mode, picture.size)
        for i in range(0, picture.size[0]):
            for j in range(0, picture.size[1]):
                pixel = picture.getpixel((i, j))  # get a pixel
                red = pixel[0]
                green = pixel[1]
                blue = pixel[2]

                if (red > red_lower_threshold and abs(green - blue) < green_blue_diff_threshold):
                    res.putpixel((i, j), pixel)
                else:
                    avg = (pixel[0] + pixel[1] + pixel[2]) / 3
                    res.putpixel((i, j), (int(avg), int(avg), int(avg)))
        res = array(res)
        return res

    def process(self, picture):
        """
        calls other class functions to process the given image
        :param picture: input image (already opened) 
        :return: output image as ARRAY 
        """
        ImageManipulator._Crop(self, picture)
        ImageManipulator._Resize(self, picture)
        return IMStop._Recolor(picture)
