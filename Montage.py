import cv2
import numpy as np
from skimage.util import montage as montage2d


# Create a Montage class
class Montage(object):

    # initialise the class using an initial image
    def __init__(self, initial_image):
        self.montage = initial_image # 1D montage
        self.imgList = [initial_image] # use to store all the images sequentially
        self.montageSize = 1 # record the size of the montage
        self.height, self.width = self.montage.shape[:2] # the height and width of the initial image

    # append the new image to the montage, reshape the height to the new image to the height of the initial image
    def append(self, image):
        height, width = image.shape[0:2] # the height and width of the new image
        # reshape the new image to have the same height as the initial image of the montage
        new_image = cv2.resize(image, (int(width * float(self.height) / height), self.height))
        # stack the images horizontally to create 1D montage
        self.montage = np.hstack((self.montage, new_image))
        # increase the montage size by 1
        self.montageSize += 1
        # append the new image to the image list
        self.imgList.append(new_image)

    # save the 1D montage
    def save(self, filename):
        cv2.imwrite(filename, self.montage)

    # save the 2D montage
    def saveMontage2D(self, filename):
        montage1d = np.array([]) # store the 1D montages with equal size as shape (n_images,height,width,channel=3)
        for img in self.imgList:
            # reshape all the images to have the same shape as initial image
            new_image = cv2.resize(img, (self.width, self.height))
            montage1d = np.append(montage1d, new_image)
        # reshape it
        montage1d = montage1d.reshape(self.montageSize, self.height, self.width, 3)
        # convert to 2d montage use montage2d function
        new_montage = montage2d(montage1d, multichannel=True)
        # save the montage
        cv2.imwrite(filename, new_montage)
