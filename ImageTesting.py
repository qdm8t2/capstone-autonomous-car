
import os
from PIL import *
from PIL import Image
from numpy import *
from pylab import *
from PIL import ImageOps
from os import listdir
from os.path import isfile, join



######################################################################################################################################################
# take in an image, convert to greyscale, convert to an image array, do some transformations, histogram equalization, convert back to an image, save #
######################################################################################################################################################
def imageprocess (String2, int2):

    #print(" \n          the following print line is from imageprocess( ) in ImageTesting.py: \n")
    #print (String2 + " was the #" + str(int2)+ " image processed")

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
def BuildCSV():
    #print(
     #   "******************************************************** \n the following print lines are from BuildCSV( ) in ImageTesting.py \n ************************************************\n")

    if not(os.path.isdir("images")):
        print("\n the provided path in the function BUILD CSV doesnt exist")
        sys.exit()
    else:
        finalValue = 0
        filesInImages = [f for f in listdir('images') if isfile(join('images' ,f))]

        try:
            filestream1 = open("fileInfoses.txt", "r+")
        except IOError:
            print(
                " Could not open textfile: fileInfoses.txt ( in function BuildCSV )")  # handle a bad filename without crashing
            sys.exit()
        line = ""
        line = line + str(0) + " ,"                                                 #note this 0 here indicates no images have been processed yet

        for p in filesInImages: line = line + p +","
        line = line + "end"



        #print("after two newlines we will print the list of images to be processed, IE what should be in the CSV file, assuming no images have been processed already\n\n")
        #print (line + "\n")
        filestream1.writelines(line)
        filestream1.truncate()
    return



###############################################################################
#                  ImageProcessing "Driver"                                   #
###############################################################################



def ImageProcessingDriver():
    finalValue = 0                                                                   # "global" var cuz im a bad programmer ( counts the number of images processed

    ############################### ENABLE/ DISABLE THIS LINE OF CODE TO REPOPULATE THE CSV WITH ALL IMAGES IN IMAGES (EXCLUDING POST) ################################

    #BuildCSV()                    #we can enable/ disable this line with comments as needed

    ############################## When THIS LINE IS ENABLED WE WILL PROCESS ALL THE IMAGES, EVEN ONES THAT HAVE ALREADY BEEN PROCESSED ################################

    #print(
        #"******************************************************** \n the following print lines are from ImageProcessingDriver( ) in ImageTesting.py \n ************************************************\n")
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
            print("in \"fileInfoses.txt\" we expect the first value in the ONE LINE CSV that ends with a the string \"end\" to be an integer,representing the No images we already have converted")     #error code
            sys.exit()                                                          #exit

        noElements = len(currentline)                                                   #get number of elements on first line
        originalValue = currentline[0]                                                 # what is the number of elements already processed, Important this value doesnt change with currentline[0]
        for i in range(1,noElements - 1):                                           # if i > than number of elements already processed then the image has yet to be processed
            if( i > originalValue | originalValue == 0):

                if i != noElements - 1 :
                        imageprocess(currentline[i], currentline[0])
                        if ( i != noElements - 2):
                            currentline[0] = int(currentline[0]) + 1   # update number of processed images
                            finalValue = int(currentline[0])
                        elif ( i == noElements - 2):                    # we dont update the count on the last one cuz there is not a next image
                            finalValue = int(currentline[0])

        print("\n\n"+str(finalValue)+ " images proceessed \n\n")
        filestream.close()


        #finally we update the CSV file to reflect the number of processed images
        try:
            filestream1 = open("fileInfoses.txt", "r+")
        except IOError:
            print(" Could not open textfile: fileInfoses.txt ( the second time )")  # handle a bad filename without crashing
            sys.exit()
        with filestream1:
            firstline = filestream1.readline()
            firstline = firstline.split(",")
            firstline[0] = str(finalValue)
            line = ""
            #line = line + str(finalValue) + " ,"  # note this 0 here indicates no images have been processed yet

            for x in firstline[:-1]: line = line + x + ","
            line = line + "end"

            filestream1.close()



            print("the following line should be written to the CSV IF FINALVALUE (# of images processed) is not zero [note this integer is the variable finalValue")
            print(" \n\n " + line + "\n\n")                                             # print the line, this is probably redundent at this point but BuildCSV is utilized differently



            try:
                filestream2 = open("fileInfoses.txt", "r+")
            except IOError:
                print(
                    " Could not open textfile: fileInfoses.txt ( the second time )")  # handle a bad filename without crashing
                sys.exit()
            with filestream2:
                if(finalValue != 0):
                    filestream2.writelines(line)
                else:
                    print("no images were processed")
    return



            #filestream1.writelines(line)

            # now we just write this line to fileInfoses.txt save and we are golden. Fix your uncatched errors and comments then do the Testing document for Capstone


    #other transformations I looked at to adjust contrast in images. Leaving here as reference for now
    #print( im.shape, im.dtype )
    #im2 = 255 - im #invert image
    #im3 =(100.0/255) * im + 100 #clamp to intervall 1000...200



def processedImagesToArray():
    #print(
        #"******************************************************** \n the following print lines are from processedImagesToArray( ) in ImageTesting.py \n ************************************************")

    if not(os.path.isdir("images/post")):
        print("\n the provided path in the function processedImagesToArray doesnt exist")
        sys.exit()
    else:
        finalValue = 0
        filesInImages = [f for f in listdir('images/post') if isfile(join('images/post' ,f))]
        line = ""
        #line = line + " ,"  # note this 0 here indicates no images have been processed yet

        for p in filesInImages:
            line = line + p + ","
            #print (p)


        line = line + "end"
        print ( "\n\n these are the images that were processed \n\n they will also be the ones converted to an array by processedImagesToArray\n\n")
        print (" \n\n" + line + " \n")
        try:
            filestream3 = open("processedImages.txt", "r+")
        except IOError:
            print(
                " Could not open textfile: processedImages.txt" )  # handle a bad filename without crashing
            sys.exit()
        with filestream3:
            filestream3.writelines(line)

        filestream3.close()

        try:
            filestream4 = open("processedImages.txt", "r+")
        except IOError:
            print(
                " Could not open textfile: processedImages.txt (the second time" )  # handle a bad filename without crashing
            sys.exit()
        with filestream4:
            lineToArray = filestream4.readline()
            lineToArray = lineToArray.split(",")
            #print("\n"+str(len(lineToArray))+"\n" +lineToArray[4])  # this is working. now just need to convert every element in lineToArray to an image array then return lineToArray

            processedImages = len(lineToArray) -1
            listOfImageArrays = []


            for i in range(0,processedImages):
                #convert the image at lineToArray[i] to an image array and place it in LineToArray[i]
                # we might actually need a new array of len(lineToArray) - 1 because the array probably cant be partially images and partially image arrays
                #print("\n"+lineToArray[i])
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









