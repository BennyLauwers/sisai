import json
from flask import request

from flask import Blueprint

import utilities.constants as cnst

from inference.ita_inference_track_and_alert import message

pass_camera_status_bp = Blueprint('pass_camera_status', __name__)

@pass_camera_status_bp.route('/api/passcamerastatus', methods=['POST'])
def pass_camera_status_post():
    result = request.json
    camera_id = result['camera_id']
    status = result['status']

    json_file = cnst.CAMERA_MGMT_JSON_FILE

    with open(json_file, 'r') as f:
        json_data = json.load(f)
        for item in json_data:
            if item['camera'] in [camera_id]:
                if status == "start":
                    item['camera_status'] = "running"
                if status == "stop":
                    item['camera_status'] = "stopped"
    
    with open(json_file, 'w') as w:
        json.dump(json_data, w, indent=4)

    message(camera_id, status)

    return json.dumps(camera_id), 200, {'ContentType': 'application/json'} 