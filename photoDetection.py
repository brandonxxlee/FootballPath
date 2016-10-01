import scipy.misc as sp

def pixelAtPosition(picture, row, col):
    return picture[row][col]
imageName = "gradientBlack.jpg"
im = sp.imread(imageName)


# Do stuff to im
im2 = sp.imresize(im, 5 )



sp.toimage(im2, cmin=0.0, cmax=...).save("next.jpg")
