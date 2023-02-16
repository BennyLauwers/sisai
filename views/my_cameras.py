import json
from flask import Blueprint
from flask import render_template

my_cameras_bp = Blueprint('my_cameras', __name__)

import utilities.constants as cnst

import utilities.def_get_camera_data as gcd

@my_cameras_bp.route('/my_cameras')
def my_cameras():
    camera_list, json_name_list, rtsp_url_list, _, zone_points_list, detection_classes_list, camera_status_list = gcd.get_camera_data(cnst.CAMERA_MGMT_JSON_FILE)
    array_rtsp_urls_list = []
    array_zone_points_list = []
    array_detection_classes = []
    array_camera_status_list = []
    for i in range(len(json_name_list)):
        array_rtsp_urls_list.append(rtsp_url_list[i])
        array_zone_points_list.append(zone_points_list[i])
        array_detection_classes.append(detection_classes_list[i])
        array_camera_status_list.append(camera_status_list[i])

    return render_template('/my_cameras/my_cameras.html', len = len(json_name_list), camera_list = camera_list, rtsp_url = array_rtsp_urls_list, detection_zone = array_zone_points_list, detection_classes = array_detection_classes, camera_status = array_camera_status_list)