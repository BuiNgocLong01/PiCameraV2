import time
import cv2
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FfmpegOutput

picam2 = Picamera2()
# video_config = picam2.create_video_configuration()
# picam2.configure(video_config)
picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (1280, 720)}))
picam2.start()

im = picam2.capture_array()
im = cv2.flip(im, 1)
            
output_dir = 'thinh_TEST/'

encoder = H264Encoder(10000000)
output = FfmpegOutput(output_dir + 'Fish_2.mp4')

picam2.start_recording(encoder, output)
time.sleep(10)

picam2.stop()
picam2.stop_recording()

 

