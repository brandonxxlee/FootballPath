import photoDetection
import meanShift
import rectangle_finder
import scipy.misc as sp
import plotter
from PIL import Image

im = photoDetection.read_in_image("water.jpg")
im = sp.imresize(im, 10)
_, im2 = photoDetection.k_means_teams(im, 10)

rects = rectangle_finder.find_rectangles(im2)
image = Image.open("images/water.jpg")
images_with_rectangles = rectangle_finder.draw_rectangles(rects, image)

pos = []
for i in im2:
    plotter.plot(i)
    pos.append(rectangle_finder.find_rectangles_for_given_locations(i))
for i in pos:
    images_with_rectangles = rectangle_finder.draw_rectangles(i, images_with_rectangles)

meanShift.save_image(images_with_rectangles)





