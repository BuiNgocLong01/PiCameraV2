#!/usr/bin/python3

import cv2

from picamera2 import Picamera2

# Grab images as numpy arrays and leave everything else to OpenCV.

face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + 
        "haarcascade_frontalface_default.xml")
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 
        "haarcascade_eye.xml"
    )
cv2.startWindowThread()

picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'RGB888', "size": (720, 480)}))
picam2.start()



def face_detect():
    window_title = "Face Detect"

    try:
        cv2.namedWindow(window_title, cv2.WINDOW_AUTOSIZE)
        while True:
            im = picam2.capture_array()
            im = cv2.flip(im, 1)

            grey = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
            faces = face_detector.detectMultiScale(grey, 1.3, 5)

            for (x, y, w, h) in faces:
                cv2.rectangle(im, (x, y), (x + w, y + h), (250, 0, 0), 2)
                roi_gray = grey[y : y + h, x : x + w]
                roi_color = im[y : y + h, x : x + w]
                eyes = eye_cascade.detectMultiScale(roi_gray)
                for (ex, ey, ew, eh) in eyes:
                    cv2.rectangle(
                        roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2
                    )
            
            if cv2.getWindowProperty(window_title, cv2.WND_PROP_AUTOSIZE) >= 0:
                cv2.imshow(window_title, im)
            else:
                break
            keyCode = cv2.waitKey(10) & 0xFF
            # Stop the program on the ESC key or 'q'
            if keyCode == 27 or keyCode == ord('q'):
                break
    finally:
        cv2.destroyAllWindows()


if __name__ == "__main__":
    face_detect()