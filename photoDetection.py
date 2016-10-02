import scipy.misc as sp

def pixelAtPosition(picture, row, col):
    return picture[row][col]
imageName = "images/footballPlayer.jpg"
im = sp.imread(imageName, flatten=True)

print (im)
print (type(im))	

im2 = sp.imfilter(im, "find_edges")
sp.toimage(im2, cmin=0.0, cmax=...).save("next.jpg")


