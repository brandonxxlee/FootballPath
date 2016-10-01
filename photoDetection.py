import scipy.misc as sp

IMAGE_FILE_PATH = './images/'


def pixel_at_position(picture, row, col):
    return picture[row][col]


def read_in_image(file_name):
    return sp.imread(file_name)

image_name = "gradientBlack.jpg"
im = read_in_image(image_name)

# Do stuff to im
im2 = sp.imresize(im, 5)


sp.toimage(im2, cmin=0.0, cmax=...).save("next.jpg")

