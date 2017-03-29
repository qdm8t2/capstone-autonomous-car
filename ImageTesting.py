
import os
from PIL import *
from PIL import Image
from numpy import *
from pylab import *
from PIL import ImageOps
from os import listdir
from os.path import isfile, join


#imageProcess
    # helper function for imageProcessingDriver reccommended only be called by other methods in this file
    # takes a single image location and an integer [the integer represents what # image we are currently on]
    # saves the image in the /post directory

def imageProcess (String2, int2):

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


#buildCSV
    #reads in a directory and builds a csv file of all the images in the directory
    #calling this sets the integer at the head of the file to zero causing all images to be reprocessed

def buildCSV():

    if not(os.path.isdir("images")):
        print("\n the provided path in the function BUILD CSV doesnt exist")
        sys.exit()
    else:
        finalValue = 0
        filesInImages = [f for f in listdir('images') if isfile(join('images' ,f))]

        
        filestream1 = csvOpen("fileInfoses.txt")
        line = ""
        line = line + str(0) + " ,"                                                 #note this 0 here indicates no images have been processed yet

        for p in filesInImages: line = line + p +","
        line = line + "end"



        #print("after two newlines we will print the list of images to be processed, IE what should be in the CSV file, assuming no images have been processed already\n\n")
        #print (line + "\n")
        filestream1.writelines(line)
        filestream1.truncate()
    return


#imageProcessingDriver
    #designed to be called from elsewhere in the project
    #uses a CSV to get all the locations of the images that should be processed
    #calles imageProcess for each image, where the image is manipulated
    #saves the image in the /post directory
    #updates the CSV to represent the # of images processed

def imageProcessingDriver():

    finalValue = 0
    filestream =csvOpen("fileInfoses.txt")            #opens a single line CSV for the file names of images to be processed

    with filestream:
        currentline = readLineSplit(filestream)    # the very first element when you split on the comma will be an integer we should check this
        try:
            currentline[0]= int(currentline[0])                 # attempt to cast the first value in the csv as an integer
        except ValueError:
            print("in \"fileInfoses.txt\" we expect the first value in the ONE LINE CSV that ends with a the string \"end\" to be an integer,representing the No images we already have converted")     #error code
            sys.exit()                                   #exit because the CSV is not as expeceted

        noElements = len(currentline)                                                   #get number of elements on first line
        originalValue = currentline[0]                                                 # what is the number of elements already processed, Important this value doesnt change with currentline[0]
        for i in range(1,noElements - 1):                                           # if i > than number of elements already processed then the image has yet to be processed
            if( i > originalValue | originalValue == 0):

                if i != noElements - 1 :
                        imageProcess(currentline[i], currentline[0])
                        if ( i != noElements - 2):
                            currentline[0] = int(currentline[0]) + 1   # update number of processed images
                            finalValue = int(currentline[0])
                        elif ( i == noElements - 2):                    # we dont update the count on the last one cuz there is not a next image
                            finalValue = int(currentline[0])

        print("\n\n"+str(finalValue)+ " images proceessed \n\n")
        filestream.close()

        #finally we update the CSV file to reflect the number of images processed

        filestream1 = csvOpen("fileInfoses.txt")
        with filestream1:
            firstline = readLineSplit(filestream1)
            firstline[0] = str(finalValue)
            line = ""
            for x in firstline[:-1]: line = line + x + ","
            line = line + "end"
            filestream1.close()

            print("the following line should be written to the CSV IF finalValue (# of images processed) is not zero")
            print(" \n\n" + line + "\n\n")

            filestream2 = csvOpen("fileInfoses.txt")
            with filestream2:
                if(finalValue != 0):
                    filestream2.writelines(line)
                else:
                    print("no images were processed")

    return

#processedImagesToArray
    #converts images in the /post directory to a list of image arrays
    #returns the list of image arrays

def processedImagesToArray():

    if not(os.path.isdir("images/post")):
        print("\n the provided path in the function processedImagesToArray doesnt exist")
        sys.exit()
    else:
        finalValue = 0
        filesInImages = [f for f in listdir('images/post') if isfile(join('images/post' ,f))]
        line = ""

        for p in filesInImages:
            line = line + p + ","

        line = line + "end"
        print ( "\n\n these are the images that were processed \n\n they will also be the ones converted to an array by processedImagesToArray\n\n")
        print (" \n\n" + line + " \n")

        filestream3 =csvOpen("processedImages.txt")
        with filestream3:
            filestream3.writelines(line)
        filestream3.close()

        filestream4 = csvOpen("processedImages.txt")
        with filestream4:
            lineToArray = readLineSplit(filestream4)

            processedImages = len(lineToArray) -1          # -1 because of "end"
            listOfImageArrays = []

            for i in range(0,processedImages):
                #convert the image at lineToArray[i] to an image array and place it in LineToArray[i]
                try:
                    if not (i == len(lineToArray)-1):
                        pil_im = Image.open("images/post/" + lineToArray[i])

                except IOError:
                    print("Could not read image " + "images/post/" + lineToArray)  # handles a bad filename
                    sys.exit()
                    # quits so cuz bad filename

                with pil_im:
                    pil_im = array(pil_im)
                    listOfImageArrays.append(pil_im)

    return listOfImageArrays



# open images
    # no open imagess method as of now since in the first open images we combine with the convert to black and white
    # this might be changed in the future as this is converted to OO


#readLineSplit
    #helper function, reccommended to only be called from within this file
    #reads a single line from open file and split it on comma
    #returns the split array

def readLineSplit(openedfile):
    splitarray = openedfile.readline()
    splitarray = splitarray.split(",")
    return splitarray


#csvOpen
    # should only be called by other methods in this file
    # returns an opened file for read and write
    # if the file location is "bad" then we exit the program saying what file we tried to open

def csvOpen(locationstring):
    try:
        openedfile = open(locationstring, "r+")
    except IOError:
        print("\n\n could not open CSV file located at: " + locationstring)
        sys.exit()
    return openedfile
