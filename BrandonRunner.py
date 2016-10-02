import photoDetection
import meanShift
import rectangle_finder
import scipy.misc as sp
import plotter
from PIL import Image

def execute(im):
    im = sp.imresize(im, 10)
    _, im2 = photoDetection.k_means_teams(im, 10)
    pos = []
    for i in im2:
        pos.append(rectangle_finder.find_rectangles_for_given_location(i))
    pos.sort(key=lambda x: sum([i*i for i in x]))
    rects = rectangle_finder.find_rectangles(im2)
    return rects
    return pos[1]


