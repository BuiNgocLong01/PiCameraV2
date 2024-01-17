import cv2
import dlib
from tkinter import *
from threading import Thread, Event
import datetime
from FaceRecOpenCV_Coppy import FaceRecongizerCV

def resize(image, width=None, height=None, inter=cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation=inter)

    # return the resized image
    return resized


class FPS:
    """Count Frame per second of video or camera stream
    """
    def __init__(self):
        # store the start time, end time, and total number of frames
        # that were examined between the start and end intervals
        self._start = None
        self._end = None
        self._numFrames = 0

    def start(self):
        # start the timer
        self._start = datetime.datetime.now()
        return self

    def stop(self):
        # stop the timer
        self._end = datetime.datetime.now()

    def update(self):
        # increment the total number of frames examined during the
        # start and end intervals
        self._numFrames += 1
        self._end = datetime.datetime.now()

    def elapsed(self):
        # return the total number of seconds between the start and
        # end interval
        return (self._end - self._start).total_seconds()

    def fps(self):
        # compute the (approximate) frames per second
        return self._numFrames / self.elapsed()


class WebcamVideoStream:
    def __init__(self, src=0, type=cv2.CAP_DSHOW):
        # initialize the video camera stream and read the first frame
        # from the stream
        self.stream = cv2.VideoCapture(src, type)
        (self.grabbed, self.frame) = self.stream.read()

        # initialize the variable used to indicate if the thread should
        # be stopped
        self.stopped = False

    def __del__(self):
        self.stream.release()

    def start(self):
        # start the thread to read frames from the video stream
        t = Thread(target=self.update, args=())
        t.daemon = True
        t.start()
        return self

    def update(self):
        # keep looping infinitely until the thread is stopped
        while True:
            # if the thread indicator variable is set, stop the thread
            if self.stopped:
                return

            # otherwise, read the next frame from the stream
            (self.grabbed, self.frame) = self.stream.read()

    def read(self):
        # return the frame most recently read
        return self.frame

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True


class CameraApp(Frame):

    def __init__(self, parent=None, cam_src=0):
        Frame.__init__(self, parent)                       # provide container
        self.pack(expand=YES, fill=BOTH)
        self.config(relief=RIDGE, border=2)                # reconfig to change
        self.video_src = cam_src
        self.cam = None
        self.frame = None
        self.stopEvent = None
        self.thread = None

        # B1: khai báo mô hình nhận diện khuôn mặt đã khai báo
        self.recognizer = FaceRecongizerCV("FaceRec_OpenCV_10sv.yml", recognizer_type='LBP') #chinh sua bo nhan dang

        # creae Gui
        self.create_gui()

    def create_gui(self):
        """Create all the necessary GUI widgets

        :return:
        """
        Label(self, text='CAMERA APPLICATION', font=("Times", 10, "bold"), relief=GROOVE, bg='light blue',
              fg='brown').pack(side=TOP, fill=BOTH)

        frame1 = Frame(master=self)
        frame1.pack(side=LEFT)
        Button(master=frame1, text='Start', command=self.on_start).pack(fill=X)
        Button(master=frame1, text='Stop', command=self.on_stop).pack(fill=X)

    def on_start(self):
        # start the thread to read frames from the video stream
        self.cam = WebcamVideoStream(self.video_src).start()
        self.frame = self.cam.read()
        cv2.namedWindow('Object Detection')
        # start the main thread to process video frame
        self.stopEvent = Event()
        self.thread = Thread(target=self.run, args=())
        self.thread.start()

    def on_stop(self):
        self.stopEvent.set()
        self.cam.stop()
        cv2.destroyAllWindows()

    def run(self):
        """This function is for the processing thread

        :return:
        """
        fps = FPS().start()
        # keep looping over frames until we are instructed to stop
        while not self.stopEvent.is_set():
            # get image from camera thread
            self.frame = self.cam.read()
            # ====================ALL PROCESSING STEPS ARE PUTTING HERE==================================
            vis = resize(self.frame, width=800)

            # B2: recognition
            image, label = self.recognizer.predict_multi_face(vis, ("unkown", "Long", "Truong", "Anh", "Nhat","Hien", "Duy", "Phuong", "Huu", "Hieu","Hung")) #goi lai hampridic
            if image is not None:
                vis = image.copy()


            # ===========================================================================================
            # draw FPS on current camera frame
            fps.update()
            cv2.putText(vis, "fps: {:7.2f}".format(fps.fps()), (10, 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            # show the camera frame to our screen
            cv2.imshow("Object Detection", vis)


if __name__ == '__main__':
    appWindow = Tk() # creates the application window (you can use any name)
    appWindow.wm_title("CAMERA APPLICATION") # displays title at the top left
    appWindow.config(bg="#037481")
    appWindow.geometry("700x600")

    csc = CameraApp(appWindow, 0)

    appWindow.mainloop()
