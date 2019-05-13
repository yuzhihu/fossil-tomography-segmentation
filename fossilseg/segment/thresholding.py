import numpy as np
from skimage.measure import label
from skimage.filters import gaussian, threshold_otsu
from skimage.morphology import closing, square, remove_small_objects
from skimage.segmentation import clear_border, slic
from skimage.color import rgb2gray
from PIL import Image

from fossilseg.segment.utils import PIL2array


def segment(img):
    image_rgb = PIL2array(img)
    image = rgb2gray(image_rgb)
    # Reverse dark and light (fossil inside is dark)
    intensity_reversed_image = 1 - image
    # Apply gaussian filter to smooth the image
    gaussian_image = gaussian(intensity_reversed_image, sigma=5)
    # Calculate global otsu threshold and apply the threshold to generate binary image
    thresh = threshold_otsu(gaussian_image)
    binary_image = closing(gaussian_image > thresh, square(3))
    # Remove objects smaller than certain size
    small_objects_removed_binary_image = remove_small_objects(binary_image, 125)
    # Remove artifacts connected to image border
    border_cleared_binary_image = clear_border(small_objects_removed_binary_image)

    label_image = label(border_cleared_binary_image)
    image_rgb[label_image > 0] = np.array([255, 0, 0])
    return Image.fromarray(image_rgb, mode='RGB')
