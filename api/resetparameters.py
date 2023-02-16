import json 

from flask import Blueprint
from flask import request

import utilities.constants as cnst

import utilities.def_get_camera_data as gcd

from api.createimage import take_picture

reset_parameters_bp = Blueprint('reset_parameters', __name__)

@reset_parameters_bp.route('/api/resetparameters', methods=['POST'])
def reset_parameters_post():
    camera_id = request.json
    json_file = cnst.CAMERA_MGMT_JSON_FILE

    camera_list, _, rtsp_url_list, _, _, _, _ = gcd.get_camera_data(json_file)
    index_value = camera_list.index(camera_id)
    rtsp_url = rtsp_url_list[index_value]

    take_picture(rtsp_url, camera_id)

    with open(json_file, 'r') as f:
        json_data = json.load(f)
        for item in json_data:
            if item['camera'] in [camera_id]:
                item['zone_points'] = []
                item['detection_classes'] = []
    with open(json_file, 'w') as file:
            json.dump(json_data, file, indent=4)

    return json.dumps(camera_id), 200, {'ContentType': 'application/json'}