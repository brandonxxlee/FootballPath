import numpy as np
import scipy.misc as sp
from sklearn.cluster import MeanShift
IMAGE_FILE_PATH = './images/'

def pixel_at_position(picture, row, col):
    return picture[row][col]

def read_in_image(file_name):
    return sp.imread(file_name)

def rgbToHue(x):
    r = x[0]
    g = x[1]
    b = x[2]
    R = r/255
    G = g/255
    B = b/255
    maxC = max(R,G,B)
    minC = min(R,G,B)
    ret = 1/(maxC - minC)
    if maxC == minC:
        return 0
    if R == maxC:
        ret *= (G-B)
    elif G == maxC:
        ret = 2.0 + (B-R)*ret
    elif B == maxC:
        ret = 4.0 + (R-G)*ret
    return (60*ret + 3600) % 360


def convertMatrixRGBToHue(matrix):
    im2 = np.zeros((m, n))
    for i in range(m):
        for j in range(n):
            im2[i][j] = rgbToHue(matrix[i][j])
    return im2

def flattenMatrix(A):
    ret = []
    for i in range(m):
        for j in range(n):
            ret.append(A[i][j])
    return np.array(ret)

def runMeanShift(X):
    ms = MeanShift(bin_seeding=True, min_bin_freq = 100)
    ft = ms.fit(X)
    labels = ft.labels_
    cluster_centers = ft.cluster_centers_      
    return labels


def buildShowPicture(labels):
    labels_unique = np.unique(labels)
    num_clusters = len(labels_unique)
    toShow = np.zeros((m, n, 3))
    maxVal = 255
    for i in range(m):
        for j in range(n):
            toShow[i][j][0] = labels[i * n + j] * maxVal * num_clusters
            toShow[i][j][1] = labels[i * n + j] * maxVal * num_clusters
            toShow[i][j][2] = labels[i * n + j] * maxVal * num_clusters
    return toShow

def freqLabel(labels):
    """
    Finds the frequency of every label in input array
    :param labels: classification for all pixels
    :return: array of frequency of labels
    """
    a = [0] * max(labels)
    for i in labels:
        a[i] += 1
    return a


image_name = IMAGE_FILE_PATH + "pats.jpg"
im = read_in_image(image_name)
# im = sp.imresize(im, 50)
m, n, k = im.shape

def execute():
    X = flattenMatrix(im)
    labels = runMeanShift(X)
    retPicture = buildShowPicture(labels)
    print(retPicture.shape)
    sp.toimage(im).save("fff.jpg")

def save_image(retPicture):
    sp.toimage(retPicture).save("compressed.jpg")
