import cv2
import time

cv2.namedWindow("Hawk Eye", 1)

capture = cv2.VideoCapture(0)


x_offset = y_offset = 50
arrows = cv2.imread('Paper.png')

while True:
    ret, webcam = capture.read()
    if ret:
        webcam[y_offset:y_offset+arrows.shape[0],
               x_offset:x_offset+arrows.shape[1]] = arrows
        cv2.imshow("Hawk Eye", webcam)
        if cv2.waitKey(10) == 27:
            break
cv2.destroyAllWindows()
