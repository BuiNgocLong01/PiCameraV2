#!/usr/bin/python3

import cv2
import time
from picamera2 import Picamera2

picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'RGB888', "size": (1280, 720)}))
picam2.start()

face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
# cv2.startWindowThread()

class FPS:
    def __init__(self):
        self.start_time = None
        self.frames = 0

    def start(self):
        self.start_time = time.time()
        return self

    def update(self):
        self.frames += 1

    def elapsed(self):
        return time.time() - self.start_time

    def fps(self):
        return self.frames / self.elapsed()
    


fps = FPS().start()

while True:
    im = picam2.capture_array()
    im = cv2.flip(im, 1)

    grey = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(grey, 1.3, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Cập nhật và hiển thị FPS
    fps.update()
    cv2.putText(im, f"FPS: {fps.fps():.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    cv2.imshow('Camera Feed', im)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the VideoCapture object
cv2.destroyAllWindows()
