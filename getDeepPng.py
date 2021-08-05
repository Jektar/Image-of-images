import copy

import imageio, os, tqdm
import numpy as np
from PIL import Image

def getAvgColor(pixelmap):
    red = []
    green = []
    blue = []
    zeros = 0
    for row in pixelmap:
        for pixel in row:
            red += [pixel[0]]
            green += [pixel[1]]
            blue += [pixel[2]]
            if pixel[0] == 0 and pixel[1] == 0 and pixel[2] == 0:
                zeros += 1

    return [sum(color)/(len(color)-zeros) for color in [red, green, blue]]

def compareColors(pixelmap1, pixelmap2):
    avg1 = getAvgColor(pixelmap1)
    avg2 = getAvgColor(pixelmap2)

    return sum([(avg1[i]-avg2[i])**2 for i in range(3)])**(1/2)

def getBestImage(pixels, smallImages, avgColors):
    r = []
    for i, simage in enumerate(smallImages):
        r += [compareColors(pixels, [[avgColors[i]]])]

    return smallImages[r.index(min(r))]

def isLegal(pos, map):
    try:
        map[pos[0]][pos[1]]
        return pos[0] >= 0 and pos[1] >= 0
    except IndexError:
        return False

def insertImage(img, smallImage, center):
    for x in range(-int(baseSize/2), int(baseSize/2)):
        for y in range(-int(baseSize/2), int(baseSize/2)):
            pixel = [p for p in smallImage[x+int(baseSize/2)][y+int(baseSize/2)]]


            if isLegal([x+center[0], y+center[1]], img) and pixel[:3] != [255, 255, 255] and pixel[:3] != [0, 0, 0]:
                if len(pixel) == 3:
                    pixel += [255]
                else:
                    pixel[3] = 255

                img[x+center[0]][y+center[1]] = [p for p in pixel]


    return img


def getExpandedImage(dim1, dim2):
    return [[[255, 255, 255, 255] for i in range(dim1)] for j in range(dim2)]

def main():
    smallImScale = 8 #how close pics are
    quality = 4 #lower is better, best is 1, but will take a LONG time (only integers)
    image = imageio.imread('mainImage.png')
    newDim = (int(image.shape[1]/quality), int(image.shape[0]/quality))
    image = np.array(Image.fromarray(image).resize(newDim))

    smallImages = [imageio.imread('smallImages/' + fileName) for fileName in os.listdir('smallImages')]
    smallImages = [np.array(Image.fromarray(img).resize([baseSize, baseSize])) for img in smallImages]
    for i, img in enumerate(smallImages): #Turn possible greyscale images into rgb
        try:
            img[0][0][0]
        except IndexError:
            smallImages[i] = np.array([[[pixel, pixel, pixel, 255] for y, pixel in enumerate(row)] for x, row in enumerate(img)])

    avgColors = [getAvgColor(simage) for simage in smallImages]
    newImage = getExpandedImage(image.shape[1]*smallImScale, image.shape[0]*smallImScale)
    

    for x in tqdm.tqdm(range(len(image))):
        for y, pixel in enumerate(image [x]):
            bestFit = getBestImage([[pixel]], smallImages, avgColors)
            newImage = insertImage(newImage, bestFit, [x*smallImScale, y*smallImScale])


    npVersion = np.array(newImage)
    imageio.imwrite('finalImg.png', npVersion[:, :, :])

if __name__ == '__main__':
    baseSize = 16
    main()