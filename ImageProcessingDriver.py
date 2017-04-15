
from ImageProcess import getImages
import ImageProcess






processer = ImageProcess.ImageProcess()                                                 # create the image processing object


def imageProcesser(images):                                             #returns a list of processed images in ARRAY FORM

    for item in images:
        processer.imageProcesser(item)
        print(item + " was the " + str(len(processer.pictures)))        # helps visualize what my code is doing
                                                                            # the greyscale function is MUUUUCH slower than the longer ImageProcesser function
    return processer.pictures                                                   # as it has to check each pixel indivudaly, then average the R+G+B values of non red
                                                                                    #pixels to manually convert each pixel to greyscale

images = getImages()                                      # commenting out this line will cause the program to not process old or new images

convertedImages = imageProcesser(images)                         #returns a list of processed IMAGES IN ARRAY FORM

print(convertedImages)                                    # shows this list of image arrays, *NOTE* FOR SOME REASON THE IMAGES PROCESSED BY GREYSCALE LOOK
                                                                # slightly different than the images processed by image processor, all the images look the
                                                                    #when they are saved. so idk have to test with quinton's code to see if I need to convert
                                                                        # all the images the same way










