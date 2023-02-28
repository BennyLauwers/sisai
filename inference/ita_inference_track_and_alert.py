import json
import os
import cv2
import numpy as np
import datetime

from multiprocessing import Process
from multiprocessing import active_children

import utilities.constants as cnst
import utilities.def_get_camera_data as gcd

import inference.ita_yolo_objectdetection as yolo
import inference.ita_init_object_trackers as trackers
import inference.ita_model_inference_and_render as inference


class Camera(object):
    def __init__(self, cam_id, rtsp, zone_points):
        self.cam_id = cam_id
        self.rtsp = rtsp
        self.zone_points = zone_points
        print("CAMERA OBJECT INITIALIZED: ", self.cam_id)

    
def get_video(cam_id, rtsp, zone_points):
    cap = cv2.VideoCapture(rtsp)
    object_detect_model = yolo.initialize_yolo()
    object_tracker_person, object_tracker_car, object_tracker_truck = trackers.initialize_object_trackers()
    object_trackers = [object_tracker_person, object_tracker_car, object_tracker_truck]

    track_id_histories = [0, 0, 0] #person = [0] / car = [1] / truck = [2] 
    
    alert_amount = 0
    today_init = datetime.datetime.now()
    json_file_init = os.path.join(cnst.CAMERA_DATA_JSON_PATH, "{}.json".format(cam_id))
    print("FILE: ", json_file_init)
    json_data_init = []
    with open(json_file_init, 'r') as f:
        json_data_init = json.load(f)
        if json_data_init == []:
            print("INIT")
            json_data_init.append({
                    "Date": today_init.strftime("%d-%m-%Y"),
                    "Alerts": 0
                })
            with open(json_file_init, 'w') as j_file:  
                json.dump(json_data_init, j_file, indent=4, separators=(',',':'))
            print("JSONS_DATA AFTER INIT: ", json_data_init)
        
        for item in json_data_init:    
            if item['Date'] == today_init.strftime("%d-%m-%Y"):
                alert_amount = item['Alerts']
    print("ALERT_AMOUNT: ", alert_amount)
    
    while (True):
        success, frame = cap.read()
        if not success:
            cap.release()
            cap = cv2.VideoCapture(rtsp)
            print('Found error; rebuilding stream')
        else:
            print(f"Camera Inference Running On: {cam_id}")
            _, track_id_histories, alert_amount = inference.model_inference_and_render(cam_id, object_detect_model, frame, object_trackers, track_id_histories, alert_amount)

 
def processes_mgmt(camera_id, status):
    json_data = []
    cam_id_register = []
    process_name_register = []

    with open(cnst.PROCESS_REGISTER_JSON_FILE, 'r') as f:
        json_data = json.load(f)
        for item in json_data:
            cam_id_register.append(item['cam_id'])
            process_name_register.append(item['process_id'])
    
    camera_list, _, rtsp_url_list, _, zone_points_list, _, _ = gcd.get_camera_data(cnst.CAMERA_MGMT_JSON_FILE)
    index_value = camera_list.index(camera_id)
    rtsp_url = rtsp_url_list[index_value]
    zone_points = zone_points_list[index_value]

    if status == "start":
        if (camera_id in cam_id_register):
            print("Camera already running")
        else:
            New_Stream = Camera(camera_id, rtsp_url, zone_points)
            New_Process = Process(target=get_video, args=(New_Stream.cam_id, New_Stream.rtsp, New_Stream.zone_points))
            New_Process.start()
            process_children = active_children()
            for process_child in process_children:
                if process_child.name not in process_name_register:
                    json_data.append({"cam_id": camera_id, "process_id": process_child.name})

                    with open(cnst.PROCESS_REGISTER_JSON_FILE, 'w') as j_file:  
                        json.dump(json_data, j_file, indent=4, separators=(',',':'))

            print("After Start: ", json_data)
    
    if status == "stop":
        if (camera_id not in cam_id_register):
            print("Camera already stopped")
        else:
            process_children = active_children()
                       
            for idx, obj in enumerate(json_data):
                if obj['cam_id'] == camera_id:
                    process_name = obj['process_id']
                    json_data.pop(idx)
            
            with open(cnst.PROCESS_REGISTER_JSON_FILE, 'w') as j_file:  
                json.dump(json_data, j_file, indent=4, separators=(',',':'))
            
            print("After stop: ", json_data)
            
            for process in process_children:
                if process.name == process_name:
                    process.kill()
                    return True

def message(camera_id, status):
        processes_mgmt(camera_id, status)