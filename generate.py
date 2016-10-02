import photoDetection
import meanShift
import rectangle_finder
from PIL import Image

im = photoDetection.read_in_image("pats.jpg")
_, im2 = photoDetection.k_means_teams(im, 10)
rects = rectangle_finder.find_rectangles(im2)
image = Image.open("images/pats.jpg")
images_with_rectangles = rectangle_finder.draw_rectangles(rects, image)
meanShift.save_image(images_with_rectangles)



