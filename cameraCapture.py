import cv2
import datetime
import time
from picamera2 import Picamera2

today = datetime.datetime.now()


picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'RGB888', "size": (640, 480)}))
picam2.start()

output_dir = 'thinh_TEST/'  

def show_camera():
    window_title = "CSI Camera"
    today = datetime.datetime.now()
    
    try:
        today = datetime.datetime.now()
        action_count = 0
        temp_min = -1

        def cond_action():
            today = datetime.datetime.now()
            if (today.minute % 1 == 0 and action_count == 0):
                return 1
            else:
                return 0

        window_handle = cv2.namedWindow(window_title, cv2.WINDOW_AUTOSIZE)

        while True:
            today = datetime.datetime.now()
            date_time = today.strftime("%M")
            
            im = picam2.capture_array()
            im = cv2.flip(im, 1)

            if cv2.getWindowProperty(window_title, cv2.WND_PROP_AUTOSIZE) >= 0:
                cv2.imshow(window_title, im)
            else:
                break
            # =========================

            if (today.minute != temp_min):
                action_count = 0
            if cond_action() == 1:
                today = datetime.datetime.now()
                img_name = "{}.png".format(date_time)
                output = output_dir + img_name
                cv2.imwrite(output, im)
                print("{} written!".format(img_name))
                action_count = 1
                temp_min = today.minute

            #time.sleep(30)
            #=========================

            keyCode = cv2.waitKey(10) & 0xFF
            if keyCode == 27 or keyCode == ord('q'):
                break
                
            if keyCode == ord('s'):
                img_name = "{}.png".format(date_time)
                cv2.imwrite(img_name, im)
                print("{} written!".format(img_name))
                
    finally:
        cv2.destroyAllWindows()


if __name__ == "__main__":
    show_camera()
