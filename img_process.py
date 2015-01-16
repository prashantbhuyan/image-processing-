__author__ = 'Prashant B. Bhuyan'



import Tkinter
import tkFileDialog
import glob
from scipy import misc
from scipy import ndimage
import numpy as np
import sys

root = Tkinter.Tk()
root.withdraw()

def applyThreshold(img):

    # apply gaussian_filter to simplify the image.  The parameter value of 3 gave me the most logical results.
    filtered_image = ndimage.gaussian_filter(img,3)

    # apply threshold by partitioning the data based on the filtered image's mean.
    binaryData = filtered_image > filtered_image.mean()

    # save the array data for filtered, binary image with threshold.
    misc.imsave('convertedImage.jpg',binaryData)

    # return true false data that has the threshold in place.
    return(binaryData)

def countObjects(img):


    # label object instances and object slices.
    slices, instances = ndimage.label(applyThreshold(img))

    # return number of object instances.
    return(instances)


def getObjectSlices(img):

    # label objects in the binary image.
    slices, instances = ndimage.label(applyThreshold(img))

    # return object slices.
    return(slices)

def centerOfMass(img):

    # find coordinates for the center of mass of all objects in the image.
    coords = ndimage.center_of_mass(img, getObjectSlices(img), range(1,countObjects(img)+1))

    # return center of mass coordinates.
    return(coords)




def main():


    sys.stdout = open("/Users/MicrostrRes/Desktop/img_process_log.txt", "w")

    # prompt the user for path to raw images.
    pathtoimages = tkFileDialog.askdirectory(title='Select Directory Containing Your Images . . .')

    # glob png formatted images together and save to variable imagefiles.
    imagefiles = glob.glob1(pathtoimages, '*.png')

    # create an array that stores each of the images.
    image_arr = [misc.imread(pathtoimages + '/' + img).astype(np.float32) for img in imagefiles]

    # initialize a counter
    count = 0

    # iterate through each image in the image_arr .
    for i in image_arr:

        count += 1


        # Print out the raw image data (without threshold) for each image.
        print '\n', 'Raw Image #', count, 'W/O Threshold:\n'
        print '\n',i,'\n'

        # Print the converted image data (with threshold) for each image.
        print '\n', 'Binary Conversion of Image #', count,'W/ Threshold:\n'
        print '\n', applyThreshold(i), '\n'

        # Print the number of objects in each image.
        print '\n', 'There are', countObjects(i), 'objects in image #', count, 'above. \n'

        # Print the objects themselves
        print '\n', 'Here are Objects (Slices) for image #', count, 'above. \n', getObjectSlices(i)

        # Print the coordinates of the center of mass for each of the objects in each image.
        print 'The Coordinates for the Center of Mass for each of the', countObjects(i), 'objects in image #', count, 'above are: \n', centerOfMass(i)
        print '********BREAK******** \n'





if __name__ == '__main__':

    main()

