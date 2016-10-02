# import cv2
import scipy.misc as sp
import numpy as np

IMAGE_FILE_PATH = './images/'


def pixel_at_position(picture, row, col):
    return picture[row][col]


def read_in_image(file_name):
    return sp.imread(IMAGE_FILE_PATH + file_name)


def manipulate_img():
    image_name = "gradientBlack.jpg"
    im = read_in_image(image_name)

    # Do stuff to im
    im2 = sp.imresize(im, 5)
    write_image(im2, "next.jpg")


def write_image(image_array, file_name):
    """
    Save the image into a specified file name
    :param image_array: ndarray to be saved
    :param file_name: file_name to hold saved image
    :return: None
    """
    sp.toimage(image_array, cmin=0.0, cmax=...).save(IMAGE_FILE_PATH + file_name)


def weighted_color_difference(color1, color2, weights=(1, 1, 1)):
    """
    Return the squared difference weighted by WEIGHTS
    :param color1: first color
    :param color2: second color
    :param weights: weights on r, g, b
    :return: weighted square difference in r, g, and b
    """
    return sum([weights[primary] * (color1[primary] - color2[primary]) ** 2 for primary in range(3)])


def k_means_teams(image_array, num_iter=100):
    """
    Runs k-means on the image_array with 3 clusters defining the
    field and the two teams on the field.
    :param image_array: ndarray of the field
    :param num_iter: number of iterations to run k_means
    :return: list of cluster centers and pixels attributed with them
    """
    rand_col = lambda: np.random.uniform(256)
    center_colors = [(rand_col(), rand_col(), rand_col()) for _ in range(3)]
    attribute_pixels = [[], [], []]

    for _ in range(num_iter):
        attribute_pixels = [[], [], []]
        new_centers = np.array([[0] * 3] * 3)
        for i in range(image_array.shape[0]):
            for j in range(image_array.shape[1]):
                current_color = pixel_at_position(image_array, i, j)
                closest_index = min(range(3),
                                    key=lambda index: weighted_color_difference(current_color, center_colors[index],
                                                                                weights=(1, 3, 1)))
                attribute_pixels[closest_index].append((i, j))
                for rgb_index in range(3):
                    new_centers[closest_index][rgb_index] += current_color[rgb_index]

        new_center_colors = []
        for center in range(3):
            if len(attribute_pixels[center]):
                new_center_colors.append(new_centers[center] / len(attribute_pixels[center]))
            else:
                new_center_colors.append(center_colors[center])

        center_colors = new_center_colors

    return center_colors, attribute_pixels


def collapse_image(image_array):
    """
    Collapses the image into three colors representing the field and two teams
    :param image_array: ndarray of the field
    :return: collapsed image
    """
    modified_image_array = np.copy(image_array)
    center_colors, attribute_pixels = k_means_teams(image_array, num_iter=10)
    for color in range(len(center_colors)):
        for pixel_position in attribute_pixels[color]:
            row, col = pixel_position
            modified_image_array[row][col] = list(center_colors[color])

    write_image(modified_image_array, 'k_means_compression.jpg')
    return modified_image_array


def edge_detection(image_array):
    """
    Edge detects football players
    :param image_array: simple image array after k means simplification
    :return: None
    """
    im2 = sp.imfilter(image_array, "find_edges")
    sp.toimage(im2, cmin=0.0, cmax=...).save("edge_detected_image.jpg")

if __name__ == '__main__':
    collapsed_img = collapse_image(read_in_image('pats.jpg'))
    edge_detection(collapsed_img)
