import meanShift
from PIL import Image, ImageDraw
import numpy as np
from sklearn.cluster import KMeans
import plotter


def runKMeans(X):
    kmeans = KMeans().fit(X)
    return kmeans.labels_

def find_rectangles(center_colors, labeled_locations, im):
    '''
    Finds the rectangles that bounds the clusters of data
    :param center_colors: colors of labels
    :param labeled_locations: ndarray of ndarrays of locations such that all locations of a subarray has a certain classification
     e.g. [ [ (1,2), (4,5) ], [ (1,1), (5,5)]] where A[0] is class 0 and A[1] is class 1
    :return: list of rectangles
    '''
    labeled_locations = remove_green(labeled_locations)
    labeled_locations = remove_white(center_colors, labeled_locations, im)
    ret = []

    for locations in labeled_locations:
        if len(locations) == 0:
            continue;
        # plotter.plot(locations)
        labels = runKMeans(locations)
        # labels = meanShift.runMeanShift(locations)
        classRectangles = find_rectangles_for_given_class(locations, labels)
        ret.extend(classRectangles)
    return ret


def find_rectangles_for_given_class(locations, labels):
    '''
    Finds the rectangles that bounds the clusters of data
    :param locations:
    :param labels: classification for each location
    :return: list of rectangles
    '''
    ret = []
    locations_for_labels = []
    for i in range(1 + max(labels)):
        locations_for_labels.append([])
    for i in range(len(locations)):
        label = labels[i]
        location = locations[i]
        locations_for_labels[label].append(location)
    for locations_for_a_label in locations_for_labels:
        rectangle = find_rectangles_for_given_locations(locations_for_a_label)
        ret.append(rectangle)
    return ret

def find_rectangles_for_given_locations(locations):
    '''
    returns top left and bottom right coordinate of all of the locations
    :param locations: list of tuples (x, y)
    :return: (top left, bottom right)
    '''
    if len(locations) == 0 or len(locations[0]) == 0:
        return [(0,0),(0,0)]
    x, y = convert_tuple_list_to_lists(locations)
    topLeftX, bottomRightX = np.percentile(x, [10,90])
    bottomRightY, topLeftY = np.percentile(y, [10,90])

    # topLeftX = min(x)
    # topLeftY = max(y)
    # bottomRightX = max(x)
    # bottomRightY = min(y)
    return [(topLeftX, topLeftY), (bottomRightX, bottomRightY)]

def convert_tuple_list_to_lists(arr):
    listTuples = list(zip(*arr))
    return list(listTuples[0]), list(listTuples[1])


def remove_green(labeled_locations):
    '''
    removes most popular classification
    :param labeled_locations:
    :return: labeled_locations without the most popular one
    '''
    green_space = max(labeled_locations, key=lambda x: len(x))
    labeled_locations.remove(green_space)
    return labeled_locations


def remove_white(center_colors, labeled_locations, im):
    """
    Removes the label associated with white color if exists
    :param labeled_locations:
    :return: labeled locations without white label
    """
    THRESHOLD = 160
    for one_label_locations in labeled_locations:
        for i in reversed(range(len(one_label_locations))):
            x, y = one_label_locations[i]
            color = im[x][y]
            if color[0] > THRESHOLD and color[1] > THRESHOLD and color[2] > THRESHOLD:
                del one_label_locations[i]
    # for i in range(len(center_colors)):
    #     color = center_colors[i]
    #     if color[0] > THRESHOLD and color[1] > THRESHOLD and color[2] > THRESHOLD:
    #         labeled_locations.remove(labeled_locations[i])

    return labeled_locations

def draw_rectangle(rect, image):
    '''
    draws onto an Image object
    :param topLeft: tuple of corner
    :param bottomRight: tuple or corner
    :param image: to draw on
    :return:
    '''
    draw = ImageDraw.Draw(image)
    topLeftt = rect[0]
    bottomRightt = rect[1]
    topLeftX = topLeftt[0]
    topLeftY = topLeftt[1]
    bottomRightX = bottomRightt[0]
    bottomRightY = bottomRightt[1]
    topRightt = (bottomRightX, topLeftY)
    bottomLeftt = (topLeftX, bottomRightY)
    lines = [[topLeftt, topRightt], [topLeftt, bottomLeftt], [bottomRightt, bottomLeftt], [bottomRightt, topRightt]]
    for line in lines:
        draw.line(line, fill=128, width=3)
    return image

def draw_rectangles(rectangle_array, image):
    ret = image
    for rect in rectangle_array:
        if len(rect) == 0 or type([]) != type(rect) or len(rect[0]) == 0:
            continue
        ret = draw_rectangle(rect, ret)
    return ret

def scaleUp(rects, resizeFactor):
    '''

    :param rects: array of array of tuples
    :param resizeFactor:
    :return:
    '''
    r = 100/resizeFactor
    for rect in rects:
        rect[0] = (rect[0][0] * r, rect[0][1] * r)
        rect[1] = (rect[1][0] * r, rect[1][1] * r)
    return rects
# def createImageObject(im):
#     m, n, k = im.shape
#     image = Image.new('RGB', (m, n))
#     image.putdata(flatten(im))
#     return image
#
# def flatten(im):
#     m, n, k = im.shape
#     ret = []
#     for i in range(m):
#         for j in range(n):
#             ret.append(im[i][j])
#     return np.array(ret)
