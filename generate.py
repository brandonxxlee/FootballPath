import photoDetection
import meanShift
import rectangle_finder

im = photoDetection.read_in_image("pats.jpg")
_, im2 = photoDetection.k_means_teams(im)

# rects = rectangle_finder.find_rectangles(im2)
# images_with_rectangles = rectangle_finder.draw_rectangles(rects, im)
# meanShift.save_image(images_with_rectangles)