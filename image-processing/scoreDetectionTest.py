import cv2
import sys
import pytesseract
from pytesseract import Output
import numpy as np

###################################################################
# THIS SCRIPT IS ONLY USED TO TEST IMAGE DETECTION ON SINGLE IMAGES
# usage: python scoreDetectionTest.py /path/to/image.png
###################################################################


# Different sorts of
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def remove_noise(image):
    return cv2.medianBlur(image,5)

def thresholding(image):
    return cv2.threshold(image, 180, 255, cv2.THRESH_BINARY_INV)[1]

def timeThresholding(image):
    return cv2.threshold(image, 150, 255, cv2.THRESH_BINARY_INV)[1]

def csgoTimeThresholding(image):
    return cv2.threshold(image, 177, 255, cv2.THRESH_BINARY_INV)[1]

def csgoRoundThresholding(image):
    return cv2.threshold(image, 155, 255, cv2.THRESH_BINARY_INV)[1]

def preprocessGameTime(image):
    im = get_grayscale(image)
    im = cv2.threshold(im, 135, 255, cv2.THRESH_BINARY_INV)[1]
    return im

def ppRightScore(image):
    im = get_grayscale(image)
    im = cv2.threshold(im, 200, 255, cv2.THRESH_BINARY_INV)[1]
    return im

#canny edge detection
def canny(image):
    return cv2.Canny(image, 100, 200)

def opening(image):
    kernel = np.ones((5,5),np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

if __name__ == '__main__':

    if len(sys.argv) < 2:
        print('u stupid')
        sys.exit()

    imPath = sys.argv[1]
    print(imPath)

    # -c tessedit_char_whitelist=0123456789

    config_csgo = ('-l eng --psm 13 -c tessedit_char_whitelist=/:0123456789')
    config_rl = ('-l Square --psm 13 -c tessedit_char_whitelist=:0123456789')

    im = cv2.imread(imPath)

    cv2.imshow('raw', im)

    im = ppRightScore(im)

    # im = get_grayscale(im)

    # im = csgoRoundThresholding(im)

    # im = csgoTimeThresholding(im)

    # im = timeThresholding(im)

    # im = thresholding(im)

    # im = opening(im)

    # im = canny(im)

    # cv2.imshow('img', im)

    print('printing text')
    text = pytesseract.image_to_string(im, config=config_rl)
    print(text)

    # d = pytesseract.image_to_data(im, output_type=Output.DICT)
    # n_boxes = len(d['level'])
    # for i in range(n_boxes):
    #     (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
    #     cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow('img', im)
    cv2.waitKey(0)
