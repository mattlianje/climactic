# USAGE
# python read_frames_slow.py --video videos/jurassic_park_intro.mp4

# import the necessary packages
from imutils.video import FPS
import argparse
import cv2
import pytesseract

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", required=True,
help="path to input video file")
args = vars(ap.parse_args())

stream = cv2.VideoCapture(args["video"])

if stream.isOpened():
    width = stream.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = stream.get(cv2.CAP_PROP_FRAME_HEIGHT)
    print("[INFO] frame dimensions width: {:.2f}".format(width))
    print("[INFO] frame dimensions height: {:.2f}".format(height))

fps = FPS().start()
frameCount = 0
framesProcessed = 0
IMAGE_OUTPUT_FOLDER = "/Users/tylerlam/Desktop/csgo-image-analysis"

def saveImg(folder, frame, count):
    filename = "%s/%s/frame%s.jpg" % (IMAGE_OUTPUT_FOLDER, folder, count)
    cv2.imwrite(filename, frame)

def getRoundTime(fr):
    x1 = 608
    x2 = x1 + 65
    y1 = 14
    y2 = y1 + 27
    return fr[y1:y2, x1:x2]

def getRound(fr):
    x1 = 642
    x2 = x1 + 33
    y1 = 42
    y2 = y1 + 15
    return fr[y1:y2, x1:x2]

def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def preproccessRoundTime(image):
    im = get_grayscale(image)
    im = cv2.threshold(im, 177, 255, cv2.THRESH_BINARY_INV)[1]
    return im

def preprocessRoundNum(image):
    im = get_grayscale(image)
    im = cv2.threshold(im, 155, 255, cv2.THRESH_BINARY_INV)[1]
    return im

def roundTimeToString(image):
    config = ('-l eng --psm 13 -c tessedit_char_whitelist=:0123456789')
    text = pytesseract.image_to_string(image, config=config)
    return text

def roundNumToString(image):
    config = ('-l eng --psm 13 -c tessedit_char_whitelist=/:0123456789')
    text = pytesseract.image_to_string(image, config=config)
    return text

# loop over frames from the video file stream
while True:
    # grab the frame from the threaded video file stream
    (grabbed, frame) = stream.read()

    # if the frame was not grabbed, then we have reached the end
    # of the stream
    if not grabbed:
        break

    frameCount += 1
    # resize the frame
    # show and save every x frames, 30fps video / 15 = Processing 2 frames per second
    if frameCount % 15 == 0:
        roundTimeImg = getRoundTime(frame)
        ppRoundTimeImg = preproccessRoundTime(roundTimeImg)
        # saveImg("round-time/raw", roundTimeImg, framesProcessed)
        # saveImg("round-time/pp", ppRoundTimeImg, framesProcessed)
        roundTime = roundTimeToString(ppRoundTimeImg)

        roundImg = getRound(frame)
        ppRoundImg = preprocessRoundNum(roundImg)
        # saveImg("round-num/raw", roundImg, framesProcessed)
        # saveImg("round-num/pp", ppRoundImg, framesProcessed)
        roundNum = roundNumToString(ppRoundImg)

        print("round time: {: >10}   round num: {: >10}    frame{:}".format(roundTime, roundNum, framesProcessed))

        framesProcessed += 1
        frameCount = 0
        cv2.imshow("Frame", frame)

    # update fps
    cv2.waitKey(1)
    fps.update()

# stop the timer and display FPS information
fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
print(framesProcessed)

# do a bit of cleanup
stream.release()
cv2.destroyAllWindows()