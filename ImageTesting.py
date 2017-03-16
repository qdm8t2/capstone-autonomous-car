
import os
from PIL import *
from PIL import Image
from numpy import *
from pylab import *
from PIL import ImageOps
from os import listdir
from os.path import isfile, join




#take in an image, convert to greyscale, convert to an image array, do some transformations, histogram equalization, convert back to an image, save'

def imageprocess (String2, int2):
    print (String2 + " was the #" + str(int2)+ " image processed")

    try:
        if not(String2 == "  "):
            pil_im = Image.open("images/" + String2 ).convert('L')                               #opens said image and converts it to greyscale

    except IOError:
        print ("Could not read image " + "images/" + String2)                               #handles a bad filename
        sys.exit()
        # quits so cuz bad filename

    with pil_im:

        #Where do we start cropping from?
        halfwidth = pil_im.size[0]/2                                            #right now I crop from the center of the image
        halfheight = pil_im.size[1]/2                                           #these two lines find the location we are cropping from, as mentioned, dead center


        #How much of the image do we want to crop out?
        width = pil_im.size[0]/2.15                                  #how much for the width
        height = pil_im.size[1]/6                                    #how much for the height

        #apply the crop line one: left edge, two: top edge, three: right edge, four: bottom

        if ((width + halfwidth) > pil_im.size[0]):
            print (" your width is out of bounds, too big the original width is " + str(pil_im.size[0]) + " your proposed size is " + str((width + halfwidth )))
            sys.exit()
        elif ((height + halfheight) > pil_im.size[1]):
            print(" your height is out of bounds, too big the original height is " + str(pil_im.size[1]) + " your proposed size is " + str((height + halfheight)))
            sys.exit()
        else:
            pil_im = pil_im.crop(
                (
                    halfwidth - width,
                    halfheight - height,
                    halfwidth + width,
                    halfheight + halfheight,                    #we want the image as close to the front of the car/ camera as possible right? so no cropping has been done for the bottom edge
                )
                )
        # define a maximum size for the image. 1000 x 1000 in this case, if we cropped too small do not save the image
        size = 1000, 1000
        if( pil_im.size[0] < size[0] & pil_im.size[1] < size[1]):
            print("Your crop has made the image too small, we would like at least a 1000 width image, your width was " + str(pil_im.size[0]))
            sys.exit()                                            #in this instance we are going to say the image is too small if BOTH the size and the width are smaller than 1000

        pil_im = array(pil_im)                                                  # convert the image to an array

        # these lines will adjust the contrast in the image
        pil_im = (100.0 / 255) * pil_im + 90                                    #clamp the values...
        pil_im = 255.0 * (pil_im / 255.0) ** 2                                  #quadratic transformation

        #convert back to an image to do the equalization
        pil_im = Image.fromarray(uint8(pil_im))
        pil_im = ImageOps.equalize(pil_im)


        # resize the image
        pil_im.thumbnail(size, Image.ANTIALIAS)                                 #we use thumbnail to preserve the aspect ratio during the resize, dont want to distort the image in any way, using our defined size

        String2 = 'images/post/newpicture0'                                                  #save transformed image as newpicture0
        String2 = String2 + str(int2)
        pil_im.save(String2+'.jpg')
    return

#############################################################################
#       Build fileInfoses.txt by taking filenames from a directory          #
#############################################################################
finalValue = 0


filesInImages = [f for f in listdir('images') if isfile(join('images' ,f))]
filestream1 = open("fileInfoses.txt", "w")
line = ""
line = line + str(0) + " ,"                                                 #note this 0 here indicates no images have been processed yet

for p in filesInImages: line = line + p +","
line = line + "end"



print("after two newlines we will print the list of images to be processed, IE what should be in the CSV file, assuming no images have been processed already\n\n")
print (line + "\n")
filestream1.writelines(line)
filestream1.truncate()



#############################################################################
try:
    filestream = open("fileInfoses.txt", "r+")            #opens a text file with one line containing comma seperated values for the file names ect
except IOError:
    print (" Could not open textfile: fileInfoses.txt" )                    #handle a bad filename without crashing
    sys.exit()
with filestream:
    currentline = filestream.readline()
    currentline = currentline.split(",")                                           # the very first element when you split on the comma will be an integer we change this value if we dont want to override our previous transformations
    try:
        currentline[0]= int(currentline[0])                 # attempt to cast the first value in the csv as an integer
    except ValueError:
        print("in \"fileInfoses.txt\" we expect the first value in the ONE LINE CSV that ends with a COMMA followed by a RETURN to be an integer, telling us how many images we already have converted")     #error code
        sys.exit()                                                          #exit

    noElements = len(currentline)                                                   #get number of elements on first line
    originalValue = currentline[0]                                                 # what is the number of elements already processed, Important this value doesnt change with currentline[0]
    for i in range(1,noElements):                                           # if i > than number of elements already processed then the image has yet to be processed
        if( i > originalValue | originalValue == 0):
            if (currentline[i] == "end"):
                filestream.close()
                filestream = open("fileInfoses.txt", "r+")                                      #close the file to start from the beginning again
                line = filestream.readline()
                line = line.split(",")
                newline= str(finalValue)+ ","
                print(newline)
                print(" the no of images processed is " + str(finalValue))                #the purpose of this is to write the number of images processed to the CSV file
                for i in range (1,len(line)):
                    newline = newline + line[i] + ","
                print(newline)
                filestream.writelines(newline)
                filestream.truncate()
                                                                        # although it doesnt actually change the first value  of the CSV [that represents # of processed images ] yet,
                                                                                                    # it does rewrite the line allowing me to change that soon

            if currentline[i] != "end":      # if its not a newline character then its going to be a file name of a preprocessing image
                    imageprocess(currentline[i], currentline[0])
                    currentline[0] = int(currentline[0]) + 1  # update number of processed images
                    finalValue = int(currentline[0])




#other transformations I looked at to adjust contrast in images. Leaving here as reference for now
#print( im.shape, im.dtype )
#im2 = 255 - im #invert image
#im3 =(100.0/255) * im + 100 #clamp to intervall 1000...200



