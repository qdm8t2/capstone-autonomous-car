
import os
from PIL import *
from PIL import Image
from numpy import *
from pylab import *
from PIL import ImageOps



#take in an image, convert to greyscale, convert to an image array, do some transformations, histogram equalization, convert back to an image, save'

def imageprocess (String2, int2):
    pil_im = Image.open("images/" + String2).convert('L')                               #opens said image converts to greyscale


    halfwidth = pil_im.size[0]/2                                            #right now I crop from the center of the image
    halfheight = pil_im.size[1]/2                                           #these two lines find the location we are cropping from, right now dead center


    twoThirdwidth = pil_im.size[0]/1.25                                     #not actually 2/3rds anymore but... whatever
    twoThirdheight = pil_im.size[1]/2.25                                    #These two lines decide how much of the image we get

    pil_im = pil_im.crop(
        (
            halfwidth - twoThirdwidth,                          #crop
            halfheight - twoThirdheight,
            halfwidth + twoThirdwidth,                          #that
            halfheight + twoThirdheight,
        )                                                       #shit
    )


    pil_im = array(pil_im)                                                  # convert the image to an array
    pil_im = (100.0 / 255) * pil_im + 100                                   #clamp the values... this might be changed a bit to offer more grey levels ( may provide higher contrast)
    pil_im = 255.0 * (pil_im / 255.0) ** 2                                  #quadratic transformation


    pil_im = Image.fromarray(uint8(pil_im))                                 #in order to do the equalization the easy way, we need an image not an array
    pil_im = ImageOps.equalize(pil_im)                                      #equalize that shit

    String2 = 'images/newpicture0'                                                  #save transformed image as newpicture#
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






#shit i was playing with to figure this stuff out, leaving it here just incase
#print( im.shape, im.dtype )
#im2 = 255 - im #invert image
#im3 =(100.0/255) * im + 100 #clamp to intervall 1000...200
#im4 = 255.0 * (im3/255.0)** 1.3 #squared
#pil_im2 = Image.fromarray(uint8(im4)).save('picture3.jpg')  #.save('picture3.jpg')
#im5 = ImageOps.equalize(im3 , mask=None)


