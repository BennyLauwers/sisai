import datetime
import os
import json

import utilities.constants as cnst

def update_json_alerts(camera_id, alert_amount):
    today = datetime.datetime.now()
    json_file = os.path.join(cnst.CAMERA_DATA_JSON_PATH, "{}.json".format(camera_id))
    json_data = []

    Flag_date_present = False  
    with open(json_file, 'r') as f:
        json_data = json.load(f)
        print("JSONS_DATA AT Start: ", json_data)
        for item in json_data:
            if item['Date'] == today.strftime("%d-%m-%Y"):
                Flag_date_present = True
                print("DATE EXISTS")
                
        if Flag_date_present:
            print("YEP INDEED DATE EXISTS")
            item['Alerts'] = alert_amount
            with open(json_file, 'w') as w:
                json.dump(json_data, w, indent=4)
            print("JSONS_DATA DATE EXISTS: ", json_data)
        else:
            print("DATE_NOT PRESENT")
            alert_amount = 1
            json_data.append({
                "Date": today.strftime("%d-%m-%Y"),
                "Alerts": alert_amount
            })
            with open(json_file, 'w') as j_file:  
                json.dump(json_data, j_file, indent=4, separators=(',',':'))
            print("JSONS_DATA DATE NOT EXISTS: ", json_data)
    
    return alert_amount