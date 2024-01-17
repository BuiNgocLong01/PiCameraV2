import time
from picamera2 import Picamera2, Preview
import cv2
import datetime


output_dir = 'thinh_TEST/' 

picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (1280, 720)}))
picam2.start()


count = 0

while True:

        while count < 10:
                # Get the current datetime


                current_time = datetime.datetime.now()

                current_second = current_time.second

                print(current_second)

                time.sleep(1)

                im = picam2.capture_array()
                im = cv2.flip(im, 1)

                cv2.imshow('thinh',im)
                

                if current_second % 5 == 0  or current_second == 0 :
                        count += 1
                        img_name = "{}.jpg".format(count)
                        output = output_dir + img_name
                        cv2.imwrite(output, im)

                else:
                        pass

                keyCode = cv2.waitKey(10) & 0xFF
                if keyCode == 27 or keyCode == ord('q'):
                        break
        break
cv2.destroyAllWindows()
