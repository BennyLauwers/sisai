import cv2
import numpy as np

from threading import Thread

from multiprocessing import Process
from multiprocessing import active_children

class WebcamVideoStream:
    def __init__(self, src=0):
        # initialize the video camera stream and read the first frame
        # from the stream
        self.stream = cv2.VideoCapture(src)
        (self.grabbed, self.frame) = self.stream.read()
        # initialize the variable used to indicate if the thread should
        # be stopped
        self.stopped = False
    def start(self):
        # start the thread to read frames from the video stream
        Thread(target=self.update, args=()).start()
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

""" class StartProcess(Process):
    def __init__(self, rtsp):
        Process.__init__(self)
        self.rtsp = rtsp

process_register = {}
def processes_mgmt(status, rtsp):
    if status == "start":
        if rtsp in process_register:
            print("Camera already running")
        else:
            start_process = StartProcess(rtsp)
            start_process.start()
            process_children = active_children()
            for process_child in process_children:
                if process_child.name not in process_register.values():
                    process_register[rtsp] = process_child.name
            print (process_register)
            return process_register
    if status == "stop":
        if rtsp not in process_register:
            print("Camera already stopped")
        else:
            process_children = active_children()
            process_name = process_register[rtsp]
            process_register.pop(rtsp)
            print("after stop: ", process_register)
            for process in process_children:
                if process.name == process_name:
                    process.kill()
                    return True """


def open_streams_overview(rtsp, zone_points, status):
    
    vs = WebcamVideoStream(src=rtsp).start()

    while True:
        frame = vs.read()
        if zone_points != [[]]:
            overlay = frame.copy()
            coordinates = np.array(zone_points, dtype=np.int32)
            cv2.fillPoly(overlay, [coordinates], (0, 12, 255))
            alpha = 0.2
            frame_w_zone = cv2.addWeighted(overlay, alpha, frame, 1-alpha, 0)
            
            ret, buffer = cv2.imencode('.jpg', frame_w_zone)
        else:
            ret, buffer = cv2.imencode('.jpg', frame)

        picture = buffer.tobytes()
        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + picture + b'\r\n')     
    vs.stop()