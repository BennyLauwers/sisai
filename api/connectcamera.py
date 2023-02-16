import json 
import os
from os.path import exists

import cv2

from flask import Blueprint
from flask import request

import utilities.constants as cnst

from api.createimage import take_picture

connect_camera_bp = Blueprint('connect_camera', __name__)


@connect_camera_bp.route('/api/connectcamera', methods=['POST'])
def connect_camera_post():
    cam_data = request.json
    camera_id = cam_data['cam_id']
    rtsp_url = cam_data['rtsp_url']

    json_file = os.path.join(cnst.CAMERA_DATA_JSON_PATH, "{}.json".format(camera_id))
    
    if exists(json_file):
        return_data = "exists"
    else:
        cap = cv2.VideoCapture(rtsp_url)
        if cap is None or not cap.isOpened():
            print('Warning: unable to open video source: ', rtsp_url)
            return_data = "not_opening"
        else:
            #create json file with dates & alerts
            entries = []
            with open(json_file, 'w') as f:
                print("The json file is created")
                json.dump(entries,f)
            
            #add camera to camera list
            listObj = []
            
            with open(cnst.CAMERA_MGMT_JSON_FILE) as f:  
                listObj = json.load(f)
            
            listObj.append({
                "camera":camera_id,
                "json-name":"{}.json".format(camera_id),
                "rtsp-url":rtsp_url,
                "picture_path":"",
                "zone_points":[],
                "detection_classes":[],
                "camera_status":""
            })

            return_data = camera_id

            with open(cnst.CAMERA_MGMT_JSON_FILE, 'w') as j_file:  
                json.dump(listObj, j_file, indent=4, separators=(',',':'))
            
            take_picture(rtsp_url, camera_id)

    return json.dumps(return_data), 200, {'ContentType': 'application/json'} 
