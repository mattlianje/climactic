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

# open a pointer to the video stream and start the FPS timer
stream = cv2.VideoCapture(args["video"])

if stream.isOpened():
    width = stream.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = stream.get(cv2.CAP_PROP_FRAME_HEIGHT)
    print("[INFO] frame dimensions width: {:.2f}".format(width))
    print("[INFO] frame dimensions height: {:.2f}".format(height))

fps = FPS().start()
frameCount = 0
framesProcessed = 0
IMAGE_OUTPUT_FOLDER = "/Users/tylerlam/Desktop/rl-image-analysis"

def saveImg(folder, frame, count):
    filename = "/%s/%s/frame%s.jpg" % (IMAGE_OUTPUT_FOLDER, folder, count)
    cv2.imwrite(filename, frame)

def getLeftScore(fr):
    x1 = 550
    x2 = x1 + 33
    y1 = 14
    y2 = y1 + 29
    return fr[y1:y2, x1:x2]

def getRightScore(fr):
    x1 = 699
    x2 = x1 + 33
    y1 = 14
    y2 = y1 + 29
    return fr[y1:y2, x1:x2]

def getGameTime(fr):
    x1 = 600
    x2 = x1 + 80
    y1 = 12
    y2 = y1 + 29
    return fr[y1:y2, x1:x2]

# to grayscale
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def preproccessRightScore(image):
    im = get_grayscale(image)
    im = cv2.threshold(im, 210, 255, cv2.THRESH_BINARY_INV)[1]
    return im

def preproccessLeftScore(image):
    im = get_grayscale(image)
    im = cv2.threshold(im, 190, 255, cv2.THRESH_BINARY_INV)[1]
    return im

def scoreToString(image):
    config = ('-l Square --psm 13 -c tessedit_char_whitelist=0123456789')
    text = pytesseract.image_to_string(image, config=config)
    return text

def preprocessGameTime(image):
    im = get_grayscale(image)
    im = cv2.threshold(im, 135, 255, cv2.THRESH_BINARY_INV)[1]
    return im

def gameTimeToString(image):
    config = ('-l Square --psm 13 -c tessedit_char_whitelist=0123456789:')
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
    # show and save every x frames
    if frameCount % 15 == 0:
        leftScoreImg = getLeftScore(frame)
        ppLeftScoreImg = preproccessLeftScore(leftScoreImg)
        leftScore = scoreToString(ppLeftScoreImg)
        # saveImg("left-score/raw", leftScoreImg, framesProcessed)
        # saveImg("left-score/pp", ppLeftScoreImg, framesProcessed)

        rightScoreImg = getRightScore(frame)
        ppRightScoreImg = preproccessRightScore(rightScoreImg)
        rightScore = scoreToString(ppRightScoreImg)
        # saveImg("right-score/raw", rightScoreImg, framesProcessed)
        # saveImg("right-score/pp", ppRightScoreImg, framesProcessed)

        gameTimeImg = getGameTime(frame)
        ppGameTimeImg = preprocessGameTime(gameTimeImg)
        gameTime = gameTimeToString(ppGameTimeImg)
        # saveImg("game-time/raw", gameTimeImg, framesProcessed)
        # saveImg("game-time/pp", ppGameTimeImg, framesProcessed)

        print("frame{:}: {: >10} {: >10} {: >10}".format(framesProcessed, leftScore, gameTime, rightScore))

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
