import json 
import os

from flask import Blueprint
from flask import request

import utilities.constants as cnst

delete_camera_bp = Blueprint('delete_camera', __name__)

@delete_camera_bp.route('/api/deletecamera', methods=['POST'])
def delete_camera_post():
    camera_id = request.json
    
    json_file_cam_mgmt = cnst.CAMERA_MGMT_JSON_FILE
    json_file_cam_data = os.path.join(cnst.CAMERA_DATA_JSON_PATH, "{}.json".format(camera_id))
    image_file = os.path.join(cnst.IMAGE_PATH, "{}.jpg".format(camera_id))
    
    #Path declaration for OS.REMOVE###################################################
    dirpath = os.path.dirname(os.path.dirname(__file__))
    c_json_file_cam_data = os.path.join(dirpath, json_file_cam_data)
    c_image_file = dirpath + image_file
    ##################################################################################

    os.remove(c_json_file_cam_data)
    os.remove(c_image_file)

    json_data_new = []
    with open(json_file_cam_mgmt, 'r') as f:
        json_data = json.load(f)
        for item in json_data:
            if item['camera'] not in [camera_id]:
                json_data_new.append(item)
    with open(json_file_cam_mgmt, 'w') as file:
            json.dump(json_data_new, file, indent=4)

    return json.dumps(camera_id), 200, {'ContentType': 'application/json'}