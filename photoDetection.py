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


def is_whiteish(color):
    DIFFERENCE_THRESHOLD = 30
    THRESHOLD = 100
    return max(color) - min(color) > DIFFERENCE_THRESHOLD and all([col > THRESHOLD for col in color])


def get_without_white_pixels(image_array):
    for row in range(image_array.shape[0]):
        for col in range(image_array.shape[1]):
            pixel_color = pixel_at_position(image_array, row, col)
            if is_whiteish(pixel_color):
                image_array[row][col] = [255, 255, 255]

    return image_array


def k_means_teams(image_array, num_iter=100):
    """
    Runs k-means on the image_array with 3 clusters defining the
    field and the two teams on the field. Removes all white pixels beforehand
    :param image_array: ndarray of the field
    :param num_iter: number of iterations to run k_means
    :return: list of cluster centers and pixels attributed with them
    """
    image_array = get_without_white_pixels(image_array)
    white_color = [255, 255, 255]
    white_pixels = []
    rand_col = lambda: np.random.uniform(256)
    center_colors = [(rand_col(), rand_col(), rand_col()) for _ in range(3)]
    attribute_pixels = [[], [], []]

    for _ in range(num_iter):
        attribute_pixels = [[], [], []]
        new_centers = np.array([[0] * 3] * 3)
        for i in range(image_array.shape[0]):
            for j in range(image_array.shape[1]):
                current_color = pixel_at_position(image_array, i, j)
                if set(current_color) != set(white_color):
                    closest_index = min(range(3),
                                        key=lambda index: weighted_color_difference(current_color, center_colors[index],
                                                                                    weights=(1, 3, 1)))
                    attribute_pixels[closest_index].append([i, j])
                    for rgb_index in range(3):
                        new_centers[closest_index][rgb_index] += current_color[rgb_index]
                else:
                    white_pixels.append([i, j])

        new_center_colors = []
        for center in range(3):
            if len(attribute_pixels[center]):
                new_center_colors.append(new_centers[center] / len(attribute_pixels[center]))
            else:
                new_center_colors.append(center_colors[center])

        center_colors = new_center_colors

    return center_colors, attribute_pixels, white_pixels


def collapse_image(image_array):
    """
    Collapses the image into three colors representing the field and two teams
    :param image_array: ndarray of the field
    :return: collapsed image
    """
    modified_image_array = np.copy(image_array)
    center_colors, attribute_pixels, white_pixels = k_means_teams(image_array, num_iter=10)
    for color in range(len(center_colors)):
        for pixel_position in attribute_pixels[color]:
            row, col = pixel_position
            modified_image_array[row][col] = list(center_colors[color])

    for pixel_position in white_pixels:
        row, col = pixel_position
        modified_image_array[row][col] = [255, 255, 0]

    write_image(modified_image_array, 'k_means_compression.jpg')
    return modified_image_array


def collapse_image_objects(image_array):
    """
    Collapses the image by white listing all of the non player pixels
    :param image_array: input image
    :return: collapsed image
    """
    THRESHOLD = 160
    modified_image_array = np.copy(image_array)
    center_colors, attribute_pixels, white_pixels = k_means_teams(image_array, num_iter=10)
    print(center_colors)
    max_color_index = max(range(3), key=lambda i: len(attribute_pixels[i]))
    for color in range(len(center_colors)):
        color_to_set = center_colors[color]
        if color == max_color_index:
            color_to_set = [255, 255, 255]
        elif color_to_set[0] > THRESHOLD and color_to_set[1] > THRESHOLD and color_to_set[2] > THRESHOLD:
            color_to_set = [255, 255, 255]
        for pixel_position in attribute_pixels[color]:
            row, col = pixel_position
            modified_image_array[row][col] = color_to_set

    write_image(modified_image_array, 'k_means_super_compressed.jpg')
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
    collapse_image(read_in_image('pats.jpg'))
