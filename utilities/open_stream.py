import cv2
import numpy as np

from threading import Thread

import utilities.yolo_objectdetection as yolo
import utilities.model_inference_and_render as inference

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

def open_stream(rtsp, zone_points, camera_id, status):
    object_detect_model = yolo.initialize_yolo()
    stream_getter = StreamGet(rtsp).start()

    while True:
        if stream_getter.stopped:
            stream_getter.stop()
            break

        frame = stream_getter.frame
        if zone_points != [[]]:
            infered_frame = inference.model_inference_and_render(camera_id, object_detect_model, frame)
            
            overlay = infered_frame.copy()
            coordinates = np.array(zone_points, dtype=np.int32)
            cv2.fillPoly(overlay, [coordinates], (0, 12, 255))
            alpha = 0.2
            frame_w_zone = cv2.addWeighted(overlay, alpha, infered_frame, 1-alpha, 0)
            
            ret, buffer = cv2.imencode('.jpg', frame_w_zone)
        else:
            infered_frame = inference.model_inference_and_render(camera_id, object_detect_model, frame)

            ret, buffer = cv2.imencode('.jpg', infered_frame)

        picture = buffer.tobytes()
        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + picture + b'\r\n')