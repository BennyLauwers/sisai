import json 
import os

import numpy as np
import cv2

from flask import Blueprint
from flask import request

import utilities.constants as cnst

get_zone_points_bp = Blueprint('get_zone_points', __name__)

@get_zone_points_bp.route('/getzonepoints', methods=['POST'])
def getzonepoints_post():
    zone_cam_data = request.json
    camera_id = zone_cam_data['camera']
    box_danger_area = zone_cam_data['zone']
    detection_classes = zone_cam_data['detection_classes']
    
    detection_classes_list = []

    for key,value in detection_classes.items():
        if value == True:
            detection_classes_list.append(key)

    json_file = cnst.CAMERA_MGMT_JSON_FILE

    image_file_path = ""
    with open(json_file, 'r') as f:
        json_data = json.load(f)
        for item in json_data:
            if item['camera'] in [camera_id]:
                item['zone_points'] = [box_danger_area]
                item['detection_classes'] = detection_classes_list
                image_file_path = item['picture_path']
    
    with open(json_file, 'w') as w:
        json.dump(json_data, w, indent=4)
    
    #Path declaration for OPENCV######################################################
    dirpath = os.path.dirname(os.path.dirname(__file__))
    file_path = dirpath + image_file_path
    ##################################################################################

    if box_danger_area != []:
        image = cv2.imread(file_path)

        overlay = image.copy()
        coordinates = np.array(box_danger_area, dtype=np.int32)
        cv2.fillPoly(overlay, [coordinates], (0, 12, 255))
        alpha = 0.2
        picture = cv2.addWeighted(overlay, alpha, image, 1-alpha, 0)

        cv2.imwrite(file_path, picture)

    return json.dumps(zone_cam_data), 200, {'ContentType': 'application/json'}