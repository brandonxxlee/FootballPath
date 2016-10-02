import photoDetection
import meanShift
import rectangle_finder
# import scipy.misc as sp
import plotter
from PIL import Image

def execute(im, resizeFactor = 100):
    '''

    :param im: 3d array with xpos, ypos, rgb
    :param resizeFactor: percent of original image
    :return:
    '''
    # im = sp.imresize(im, resizeFactor)
    center_colors, im2 = photoDetection.k_means_teams(im, 10)
    rects = rectangle_finder.find_rectangles(center_colors, im2, im)
    rects = rectangle_finder.scaleUp(rects, resizeFactor)

    # pos = []
    # for i in im2:
    #     # plotter.plot(i)
    #     pos.append(rectangle_finder.find_rectangles_for_given_locations(i))
    # pos = rectangle_finder.scaleUp(pos, resizeFactor)
    # rects.extend(pos)
    rects.sort(key=lambda x: sum([ (rect[0][1] - rect[1][1])**2 + (rect[0][1] - rect[1][1])**2  for rect in rects]))
    return rects[-1]
