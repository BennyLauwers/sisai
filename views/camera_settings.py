import json

from flask import Blueprint
from flask import render_template

my_camera_settings_bp = Blueprint('my_camera_settings', __name__)

import utilities.constants as cnst

import utilities.def_get_camera_data as gcd

@my_camera_settings_bp.route('/my_cameras/settings/<camera_id>')
def my_camera_settings(camera_id):
    camera_list, json_name_list, rtsp_url_list, _, _, detection_classes_list, status_list = gcd.get_camera_data(cnst.CAMERA_MGMT_JSON_FILE)
    index_value = camera_list.index(camera_id)
    csv_file = json_name_list[index_value]
    rtsp_url = rtsp_url_list[index_value]
    detection_classes = detection_classes_list[index_value]
    status = status_list[index_value]
    
    with open(cnst.CAMERA_MGMT_JSON_FILE) as f:
        data = json.load(f)
        image_file_path = ""
        for item in data:
            if item['camera'] in [camera_id]:
                if item['zone_points'] == []:
                    zone_ok = False
                else:
                    zone_ok = True
                if item['picture_path'] == "":
                    image_ok = False
                else:
                    image_ok = True
                    image_file_path = item['picture_path']

    return render_template(
        "/my_cameras/settings/camera_settings.html",
        csv_file=csv_file,
        rtsp_url=rtsp_url,
        camera = camera_id,
        image_exists = image_ok,
        path = image_file_path,
        zone_ok = zone_ok,
        detection_classes = detection_classes,
        camera_list=camera_list,
        status = status
        )