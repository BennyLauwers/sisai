import json 
import os

import cv2

from flask import Blueprint
from flask import request

import utilities.constants as cnst

import utilities.def_get_camera_data as gcd

create_image_bp = Blueprint('create_image', __name__)

def take_picture(rtsp_url, camera_id):
    #Path declaration for OPENCV######################################################
    dirpath = os.path.dirname(os.path.dirname(__file__))
    file_path = os.path.join(dirpath, "static", "images", "{}.jpg".format(camera_id))
    ##################################################################################
    image_file_path = os.path.join(cnst.IMAGE_PATH, "{}.jpg".format(camera_id))
    
    vs = cv2.VideoCapture(rtsp_url)
    
    success, frame = vs.read()  # read the camera frame
    if not success:
        print("CANNOT OPEN CAMERA")
    else:
        picture = frame

        vs.release()

    cv2.imwrite(file_path, picture)

    json_file = cnst.CAMERA_MGMT_JSON_FILE

    with open(json_file, 'r') as f:
        json_data = json.load(f)
        for item in json_data:
            if item['camera'] in [camera_id]:
                item['picture_path'] = image_file_path
    
    with open(json_file, 'w') as w:
        json.dump(json_data, w, indent=4)
    
    return file_path

@create_image_bp.route('/api/createimage', methods=['POST'])
def take_picture_post():
    camera_id = request.json
    camera_list, _, rtsp_url_list, _, _, _, _ = gcd.get_camera_data(cnst.CAMERA_MGMT_JSON_FILE)
    index_value = camera_list.index(camera_id)
    rtsp_url = rtsp_url_list[index_value]

    image_file_path = take_picture(rtsp_url, camera_id)

    return json.dumps(image_file_path), 200, {'ContentType': 'application/json'} 