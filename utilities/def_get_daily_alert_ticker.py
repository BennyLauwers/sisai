import json

import utilities.constants as cnst

def get_daily_alert_ticker(json_camera_alert_file):    
    todays_alert_values = 0
    yesterday_alert_values = 0

    with open(json_camera_alert_file) as f:
        data = json.load(f)
        for item in data:
            if item['Date'] in [cnst.TODAY_FORMATTED]:
                todays_alert_values = item['Alerts']
            if item['Date'] in [cnst.YESTERDAY_FORMATTED]:
                yesterday_alert_values = item['Alerts']
    
    alerts_delta = todays_alert_values - yesterday_alert_values     

    return todays_alert_values, alerts_delta