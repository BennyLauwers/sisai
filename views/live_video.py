import json

from flask import Blueprint
from flask import render_template

import utilities.constants as cnst

import utilities.def_get_camera_data as gcd
import utilities.def_get_daily_alert_ticker as gdat

live_video_bp = Blueprint('livestream', __name__)

@live_video_bp.route('/livestream/<camera_id>')
def live(camera_id):
    camera_list, json_name_list, rtsp_url_list, _, _, _, _ = gcd.get_camera_data(cnst.CAMERA_MGMT_JSON_FILE)
    array_todays_alert_values = []
    array_delta_values = []
    array_json_file_list = []
    
    for i in range(len(camera_list)):
        todays_alert_values, alerts_delta = gdat.get_daily_alert_ticker(cnst.CAMERA_DATA_JSON_PATH+json_name_list[i])
        array_json_file_list.append(json_name_list[i])
        array_todays_alert_values.append(todays_alert_values)
        array_delta_values.append(alerts_delta)
    
    index_value = camera_list.index(camera_id)
    camera = camera_list[index_value]
    alert_value = array_todays_alert_values[index_value]
    delta_value = array_delta_values[index_value]

    if rtsp_url_list[index_value] == "":
        rtsp_present = False
    else:
        rtsp_present = True
    
    json_file = array_json_file_list[index_value]

    date_value = ""
    with open(cnst.CAMERA_DATA_JSON_PATH+json_file) as f:
        data = json.load(f)
        for item in data:
            if item['Date'] in [cnst.TODAY_FORMATTED]:
                date_value = item["Alerts"]

    return render_template(
        '/livestream/livestream.html',
        rtsp_present = rtsp_present,
        len = len(camera_list),
        camera_list = camera_list,
        todays_alert_values=array_todays_alert_values,
        delta = array_delta_values,
        camera = camera,
        alert_value = alert_value,
        delta_value = delta_value,
        dates=[cnst.TODAY_FORMATTED],
        alerts=[date_value]
        )