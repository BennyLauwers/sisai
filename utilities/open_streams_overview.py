import cv2
import numpy as np

from threading import Thread

class StreamGet:
    """
    Class that continuously gets frames from a VideoCapture object
    with a dedicated thread.
    """
    def __init__(self, src=0):
        self.stream = cv2.VideoCapture(src)
        (self.grabbed, self.frame) = self.stream.read()
        self.stopped= False
    
    def start(self):
        Thread(target=self.get, args=()).start()
        print("GET TREATH STARTED")
        return self
        
    def get(self):
        while not self.stopped:
            if not self.grabbed:
                self.stop()
            else:
                (self.grabbed, self.frame) = self.stream.read()
    
    def stop(self):
        self.stopped = True

def open_streams_overview(rtsp, zone_points, status):
    stream_getter = StreamGet(rtsp).start()

    while True:
        if stream_getter.stopped:
            stream_getter.stop()
            break

        frame = stream_getter.frame
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