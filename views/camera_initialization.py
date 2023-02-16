import json

from flask import Blueprint
from flask import render_template

camera_initialization_bp = Blueprint('camera_initialization', __name__)

import utilities.constants as cnst

import utilities.def_get_camera_data as gcd

@camera_initialization_bp.route('/my_cameras/settings/camera_initialization/<camera_id>')
def my_camera_settings(camera_id):
    camera_list, json_name_list, rtsp_url_list, _, _, _, _ = gcd.get_camera_data(cnst.CAMERA_MGMT_JSON_FILE)
    index_value = camera_list.index(camera_id)
    csv_file = json_name_list[index_value]
    rtsp_url = rtsp_url_list[index_value]
    
    with open(cnst.CAMERA_MGMT_JSON_FILE) as f:
        data = json.load(f)
        image_file_path = ""
        for item in data:
            if item['camera'] in [camera_id]:
                if item['picture_path'] == "":
                    image_ok = False
                else:
                    image_ok = True
                    image_file_path = item['picture_path']

    return render_template(
        "/my_cameras/settings/camera_initialization.html",
        csv_file=csv_file,
        rtsp_url=rtsp_url,
        camera = camera_id,
        image_exists = image_ok,
        path = image_file_path,
        camera_list=camera_list
        )