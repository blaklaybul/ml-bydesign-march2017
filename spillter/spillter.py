import cv2
import numpy as np


# Read-in source image using Open CV, convert to a 4 channel bitmap
img = cv2.imread('resources/sea-water-ocean-waves.jpg')
img_3chan = cv2.imread('resources/sea-water-ocean-waves.jpg', cv2.IMREAD_UNCHANGED)
b,g,r = cv2.split(img_3chan)
alpha = np.ones(b.shape, dtype=b.dtype) * 255
img_4chan = cv2.merge((b, g, r, alpha))


# Basic Line detection using the out-of-the-box OpenCV "Canny" effect. 
# Results in a black/white line depiction that is then inverted so it can be applied as a mask. 
# Ultimately this code was not used in creating the final project result

# edges = cv2.Canny(img, 100,200)
# inverted = 255 - edges
# trans = np.ones((img.shape[0],img.shape[1],4))
# trans[:][:][inverted==0] = [0,0,0,255]
# trans[:][:][inverted==255] = [255,255,255,0]


# Input here should be the result of the Source image run through Somatic's Oil
# effect.  This creates a line effect that is similar to openCV's "Canny" effect
# however has thicker lines and a general 'splotchiness' that creates a better looking
# result than simple line detection.
oil = cv2.imread('resources/sea-water-ocean-waves_somatic_oil.jpg', 0)

# Make sure source, modified source are the same dimensions
oil_img_3chan = cv2.resize(oil, (2592, 1728))

# Convert the dark lines of the modified source to blacks
ret,thresh1 = cv2.threshold(oil_img_3chan, 40, 255,cv2.THRESH_BINARY)

# Combine source and modified images and output result
img_4chan[:][:][thresh1==0] = [0,0,0,255]
cv2.imwrite('resources/horse1_outlines_result.png', img_4chan)
