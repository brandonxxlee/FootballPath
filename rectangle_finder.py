import meanShift
from PIL import Image, ImageDraw


def find_rectangles(labeled_locations):
    '''
    Finds the rectangles that bounds the clusters of data
    :param labeled_locations: ndarray of ndarrays of locations such that all locations of a subarray has a certain classification
     e.g. [ [ (1,2), (4,5) ], [ (1,1), (5,5)]] where A[0] is class 0 and A[1] is class 1
    :return: list of rectangles
    '''
    labeled_locations = remove_green(labeled_locations)
    ret = []
    for locations in labeled_locations:
        labels = meanShift.runMeanShift(locations)
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
    locations_for_labels = [[]] * max(labels) # all the locations for a given label
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
    x, y = convert_tuple_list_to_lists(locations)
    topLeftX = min(x)
    topLeftY = max(y)
    bottomRightX = max(x)
    bottomRightY = min(y)
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

def draw_rectangle(rect, image):
    '''
    draws onto an Image object
    :param topLeft: tuple of corner
    :param bottomRight: tuple or corner
    :param image: to draw on
    :return:
    '''
    draw = ImageDraw.Draw(image)
    draw.line(rect, fill=128, width=3)
    return image

def draw_rectangles(rectangle_array, image):
    ret = image
    for rect in rectangle_array:
        ret = draw_rectangle(rect, ret)
    return ret
