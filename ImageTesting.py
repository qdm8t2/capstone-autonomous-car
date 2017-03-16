
import os
from PIL import *
from PIL import Image
from numpy import *
from pylab import *
from PIL import ImageOps



#take in an image, convert to greyscale, convert to an image array, do some transformations, histogram equalization, convert back to an image, save'

def imageprocess (String2, int2):

    pil_im = Image.open("images/" + String2).convert('L')                               #opens said image and converts it to greyscale


    #Where do we start cropping from?

    halfwidth = pil_im.size[0]/2                                            #right now I crop from the center of the image
    halfheight = pil_im.size[1]/2                                           #these two lines find the location we are cropping from, as mentioned, dead center



    #How much of the image do we want to crop out?
    width = pil_im.size[0]/2.15                                  #how much for the width
    height = pil_im.size[1]/6                                    #how much for the height


    #apply the crop line one: left edge, two: top edge, three: right edge, four: bottom
    pil_im = pil_im.crop(
        (
            halfwidth - width,
            halfheight - height,
            halfwidth + width,
            halfheight + halfheight,                    # we want the image as close to the car as possible right? so no cropping done for the bottom edge
        )
    )

    pil_im = array(pil_im)                                                  # convert the image to an array


    # these lines will adjust the contrast in the image
    pil_im = (100.0 / 255) * pil_im + 90                           #clamp the values...
    pil_im = 255.0 * (pil_im / 255.0) ** 2                                  #quadratic transformation


    pil_im = Image.fromarray(uint8(pil_im))                                 #in order to do the equalization the easy way, we need an image not an array
    pil_im = ImageOps.equalize(pil_im)                                      #equalize the image

    size = 1000 , 1000                                                  #define a maximum size for the image. 1000 x 1000 in this case

    pil_im.thumbnail(size, Image.ANTIALIAS)                                 #we use thumbnail to preserve the aspect ratio during the resize, dont want to distort the image in any way

    String2 = 'images/newpicture0'                                                  #save transformed image as newpicture0
    String2 = String2 + str(int2)
    pil_im.save(String2+'.jpg')
    return


with open("fileInfoses.txt", "r+") as filestream:                               #opens a text file with one line containing comma seperated values for the file names ect
    for line in filestream:
        currentline = line.split(",")                                           # the very first element when you split on the comma will be an integer we change this value if we dont want to override our previous transformations
        noElements = len(currentline)
        for i in range(1,noElements):                                           # i thought i would be clever and not need to mess with newlines or end of file
            print (currentline[i])
            if currentline[i] != "\n":                                                  # but it didnt work
                imageprocess(currentline[i],currentline[0])
                currentline[0] = int(currentline[0]) + 1                                #increment the first int, so the images arent saved over eachother

    filestream.truncate()






#other transformations I looked at to adjust contrast in images. Leaving here as reference for now
#print( im.shape, im.dtype )
#im2 = 255 - im #invert image
#im3 =(100.0/255) * im + 100 #clamp to intervall 1000...200



