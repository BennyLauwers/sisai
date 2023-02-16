import json 
import datetime
from datetime import timedelta

from flask import Blueprint
from flask import request

import utilities.constants as cnst

import utilities.def_get_camera_data as gcd

get_days_span_bp = Blueprint('get_days_span', __name__)

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

@get_days_span_bp.route('/api/getdaysspan', methods=['POST'])
def getdaysspan_post():
    camera_list, json_name_list, _, _, _, _, _ = gcd.get_camera_data(cnst.CAMERA_MGMT_JSON_FILE)
    days_span = request.json
    date_span = days_span['date_span']
    start_date = cnst.TODAY - datetime.timedelta(date_span)

    array_json_file_list = []
    for i in range(len(camera_list)):
        array_json_file_list.append(cnst.CAMERA_DATA_JSON_PATH+json_name_list[i])
    
    camera_id = days_span['camera']
    index_value = camera_list.index(camera_id)
    json_file = array_json_file_list[index_value]

    dates_list = []
    alerts_list = []

    with open(json_file) as f:
        data = json.load(f)
        for single_date in daterange((start_date+timedelta(1)), (cnst.TODAY+timedelta(1))):
            single_date_formatted = single_date.strftime('%d-%m-%Y')
            for item in data:
                if item['Date'] in [single_date_formatted]:
                    dates_list.append(item['Date'])
                    alerts_list.append(item['Alerts'])

    zip_iterator = zip(dates_list, alerts_list)
    alert_dictionary = dict(zip_iterator)
    
    return json.dumps(alert_dictionary), 200, {'ContentType': 'application/json'}