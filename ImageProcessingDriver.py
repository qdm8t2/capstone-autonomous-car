from ImageProcessing.ImageTesting import ImageProcessingDriver
from ImageProcessing.ImageTesting import processedImagesToArray
from ImageProcessing.ImageTesting import BuildCSV


#image testing has 4 functions
#BuildCSV looks at the /images directory and builds a comma seperated value file with all the image names
#ImageProcessingDriver uses that CSV to manipulate the images, convert to B&W, crop, resize, equalize ect
    #ImageProcessingDriver calls #imageprocess to do a lot of this work
#processedImagesToArray will convert the images in images/post/ to image arrays to be manipulated by the nerual net


BuildCSV()                                      # commenting out this line will cause the program to not process old or new images
ImageProcessingDriver()                         # does most of the work


list = processedImagesToArray()
print(list)
