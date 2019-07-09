# Importing the libraries
import cv2

# Loading the cascades
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
smile_cascade = cv2.CascadeClassifier('haarcascade_smile.xml')

# Defining a function that will do the detections
def detect(gray, frame):#gray is the greyscale version of the image the webcam will take and frame is the original image
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)#face detector
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)#the rectangle that will surround the face which will be blue in color ( 255,0,0 -> blue )
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 22)#eye detector
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2) #same as face except green in color
        smiles = smile_cascade.detectMultiScale(roi_gray, 1.7, 10)
        for (sx, sy, sw, sh) in smiles:
            cv2.rectangle(roi_color, (sx, sy), (sx+sw, sy+sh), (0, 0, 255), 2) # red ib color that detects smile and you may need to change the value of threshold . Here , I used 50
    return frame #we return the original frame , because we want colored output

# Doing some Face Recognition with the webcam
video_capture = cv2.VideoCapture(0)# starting the webcam
while True:
    _, frame = video_capture.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)#converting to grayscale.
    canvas = detect(gray, frame)
    cv2.imshow('Video', canvas)#showing the video feed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
video_capture.release()
cv2.destroyAllWindows()#destroying the windows after it quits 
