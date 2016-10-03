import photoDetection
import meanShift
import rectangle_finder
import scipy.misc as sp
import plotter
from PIL import Image

water = "water.jpg"
pats = "pats.jpg"
fb = "footballPlayer.jpg"
img = pats

resizeFactor = 10

im = photoDetection.read_in_image(img)
im = sp.imresize(im, resizeFactor)
center_colors, im2, white_colors = photoDetection.k_means_teams(im, 10)
rects = rectangle_finder.find_rectangles(center_colors, im2, im)
image = Image.open("images/" + img)
rects = rectangle_finder.scaleUp(rects, resizeFactor)
rects = rects[len(rects)//2:]
images_with_rectangles = rectangle_finder.draw_rectangles(rects, image)

# pos = []
# for i in im2:
#     #plotter.plot(i)
#     pos.append(rectangle_finder.find_rectangles_for_given_locations(i))
# pos = rectangle_finder.scaleUp(pos, resizeFactor)
# images_with_rectangles = rectangle_finder.draw_rectangles(pos, images_with_rectangles)

meanShift.save_image(images_with_rectangles)





